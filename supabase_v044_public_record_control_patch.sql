-- BowlMeet v0.4.4-dev.1 | Public Record Control compatibility patch
-- Execute once in Supabase SQL Editor before testing "取消公開" across devices.
-- Safe intent: only replaces bowling_group_push; no table data is deleted by this migration.

create or replace function public.bowling_group_push(
  p_group_code text,
  p_pin text,
  p_payload jsonb,
  p_base_revision bigint,
  p_device_id text,
  p_device_name text
) returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  r public.bowling_groups%rowtype;
  v_hash text := encode(digest(trim(coalesce(p_pin,'')),'sha256'),'hex');
  v_name text;
  v_payload jsonb := coalesce(p_payload,'{}'::jsonb);
  v_control_map jsonb := '{}'::jsonb;
  v_controls jsonb := '[]'::jsonb;
  v_sessions_before jsonb := '[]'::jsonb;
  v_sessions_after jsonb := '[]'::jsonb;
  v_meetups_after jsonb := '[]'::jsonb;
  v_item jsonb;
  v_old jsonb;
  v_id text;
  v_new_stamp bigint;
  v_old_stamp bigint;
begin
  select * into r
  from public.bowling_groups
  where group_code=upper(trim(coalesce(p_group_code,''))) and pin_hash=v_hash
  for update;
  if not found then
    return jsonb_build_object('ok',false,'error','not_found_or_pin');
  end if;
  if coalesce(p_base_revision,0) <> r.revision then
    return jsonb_build_object(
      'ok',false,
      'conflict',true,
      'revision',r.revision,
      'group_code',r.group_code,
      'group_name',r.group_name,
      'payload',r.payload
    );
  end if;

  -- v0.4.4-dev.1: PUBLIC history keeps record-control tombstones server-side.
  -- Older clients may omit recordControls; existing controls are still retained
  -- and removed sessions are filtered so an old payload cannot resurrect them.
  if r.group_code in ('PUBLIC','DEV442','V44D22','V44D33','V44D44','V44R22','V45D22','V45D23') then
    for v_item in
      select value from jsonb_array_elements(coalesce(r.payload->'recordControls','[]'::jsonb))
    loop
      v_id := trim(coalesce(v_item->>'id',''));
      if v_id <> '' then
        v_control_map := jsonb_set(v_control_map,array[v_id],v_item,true);
      end if;
    end loop;

    for v_item in
      select value from jsonb_array_elements(coalesce(v_payload->'recordControls','[]'::jsonb))
    loop
      v_id := trim(coalesce(v_item->>'id',''));
      if v_id <> '' then
        v_old := v_control_map->v_id;
        v_new_stamp := case when coalesce(v_item->>'updatedAt','') ~ '^[0-9]+$' then (v_item->>'updatedAt')::bigint else 0 end;
        v_old_stamp := case when coalesce(v_old->>'updatedAt','') ~ '^[0-9]+$' then (v_old->>'updatedAt')::bigint else 0 end;
        if v_old is null or v_new_stamp >= v_old_stamp then
          v_control_map := jsonb_set(v_control_map,array[v_id],v_item,true);
        end if;
      end if;
    end loop;

    select coalesce(jsonb_agg(value),'[]'::jsonb)
      into v_controls
    from jsonb_each(v_control_map);

    v_sessions_before := coalesce(v_payload->'sessions','[]'::jsonb);

    select coalesce(jsonb_agg(s),'[]'::jsonb)
      into v_sessions_after
    from jsonb_array_elements(v_sessions_before) as x(s)
    where coalesce(((v_control_map -> (s->>'id')) ->> 'state'),'published') <> 'removed';

    select coalesce(jsonb_agg(m),'[]'::jsonb)
      into v_meetups_after
    from jsonb_array_elements(coalesce(v_payload->'meetups','[]'::jsonb)) as x(m)
    where
      not exists (
        select 1
        from jsonb_array_elements(v_sessions_before) as y(s)
        where s->>'meetupId'=m->>'id'
          and coalesce(((v_control_map -> (s->>'id')) ->> 'state'),'published')='removed'
      )
      or exists (
        select 1
        from jsonb_array_elements(v_sessions_after) as y(s)
        where s->>'meetupId'=m->>'id'
      );

    v_payload := jsonb_set(v_payload,'{sessions}',v_sessions_after,true);
    v_payload := jsonb_set(v_payload,'{meetups}',v_meetups_after,true);
    v_payload := jsonb_set(v_payload,'{recordControls}',v_controls,true);
    v_payload := jsonb_set(v_payload,'{schema}','2'::jsonb,true);
  end if;

  v_name := left(coalesce(nullif(v_payload #>> '{groupName}',''),r.group_name),80);
  update public.bowling_groups
  set payload=v_payload,
      group_name=v_name,
      revision=revision+1,
      updated_at=now(),
      updated_by=coalesce(p_device_id,'')
  where group_code=r.group_code
  returning * into r;
  return jsonb_build_object(
    'ok',true,
    'revision',r.revision,
    'group_code',r.group_code,
    'group_name',r.group_name,
    'payload',r.payload,
    'updated_at',r.updated_at,
    'updated_by',r.updated_by
  );
end;
$$;


revoke all on function public.bowling_group_push(text,text,jsonb,bigint,text,text) from public;
grant execute on function public.bowling_group_push(text,text,jsonb,bigint,text,text) to anon, authenticated;

notify pgrst, 'reload schema';
