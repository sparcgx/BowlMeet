-- BowlMeet v0.4.2-R3
-- Personal PIN Change RPC hotfix
-- Safe to run multiple times.

create or replace function public.bowling_player_change_pin(
  p_player_id text,
  p_current_pin text,
  p_new_pin text,
  p_device_id text,
  p_device_name text
) returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $pin_change$
declare
  r public.bowling_player_profiles%rowtype;
  v_current_hash text := encode(digest(trim(coalesce(p_current_pin,'')),'sha256'),'hex');
  v_new_pin text := trim(coalesce(p_new_pin,''));
  v_new_hash text;
begin
  if length(v_new_pin) <> 6 or v_new_pin ~ '[^0-9]' then
    return jsonb_build_object('ok',false,'error','invalid_new_pin');
  end if;

  if trim(coalesce(p_current_pin,'')) = v_new_pin then
    return jsonb_build_object('ok',false,'error','same_pin');
  end if;

  select * into r
  from public.bowling_player_profiles
  where player_id = upper(trim(coalesce(p_player_id,'')))
    and pin_hash = v_current_hash
  for update;

  if not found then
    return jsonb_build_object('ok',false,'error','not_found_or_pin');
  end if;

  v_new_hash := encode(digest(v_new_pin,'sha256'),'hex');

  update public.bowling_player_profiles
  set pin_hash = v_new_hash,
      revision = revision + 1,
      updated_at = now(),
      updated_by = coalesce(p_device_id,'')
  where player_id = r.player_id
  returning * into r;

  return jsonb_build_object(
    'ok',true,
    'revision',r.revision,
    'player_id',r.player_id,
    'display_name',r.display_name,
    'updated_at',r.updated_at
  );
end;
$pin_change$;

revoke all on function public.bowling_player_change_pin(text,text,text,text,text) from public;
grant execute on function public.bowling_player_change_pin(text,text,text,text,text) to anon, authenticated;

notify pgrst, 'reload schema';

-- Optional verification query:
-- select routine_schema, routine_name
-- from information_schema.routines
-- where routine_schema='public'
--   and routine_name='bowling_player_change_pin';
