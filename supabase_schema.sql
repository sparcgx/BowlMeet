-- 保齡球球聚｜BowlMeet v0.4.1｜Player Claim & Personal Score Sync
-- 在 Supabase > SQL Editor 執行一次。
-- 房間資料只透過 SECURITY DEFINER RPC 存取；不直接開放資料表給 anon/authenticated。

create extension if not exists pgcrypto;

create table if not exists public.bowling_sync_rooms (
  room_code text primary key,
  pin_hash text not null,
  payload jsonb not null default '{}'::jsonb,
  presence jsonb not null default '{}'::jsonb,
  revision bigint not null default 1,
  updated_at timestamptz not null default now(),
  updated_by text not null default ''
);

alter table public.bowling_sync_rooms enable row level security;
revoke all on table public.bowling_sync_rooms from anon, authenticated;

create or replace function public.bowling_room_create(
  p_room_code text,
  p_pin text,
  p_payload jsonb,
  p_device_id text,
  p_device_name text
) returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  v_code text := upper(trim(coalesce(p_room_code,'')));
  v_pin text := trim(coalesce(p_pin,''));
  v_hash text;
  v_presence jsonb;
begin
  if v_code !~ '^[A-Z2-9]{6}$' then
    return jsonb_build_object('ok',false,'error','invalid_room_code');
  end if;
  if v_pin !~ '^[0-9]{6}$' then
    return jsonb_build_object('ok',false,'error','invalid_pin');
  end if;
  if exists(select 1 from public.bowling_sync_rooms where room_code=v_code) then
    return jsonb_build_object('ok',false,'error','room_exists');
  end if;
  v_hash := encode(digest(v_pin,'sha256'),'hex');
  v_presence := jsonb_build_object(
    coalesce(nullif(p_device_id,''),'unknown'),
    jsonb_build_object(
      'deviceId',coalesce(nullif(p_device_id,''),'unknown'),
      'name',coalesce(nullif(p_device_name,''),'裝置'),
      'role','host',
      'lastSeen',(extract(epoch from clock_timestamp())*1000)::bigint
    )
  );
  insert into public.bowling_sync_rooms(room_code,pin_hash,payload,presence,revision,updated_at,updated_by)
  values(v_code,v_hash,coalesce(p_payload,'{}'::jsonb),v_presence,1,now(),coalesce(p_device_id,''));
  return jsonb_build_object('ok',true,'revision',1,'payload',coalesce(p_payload,'{}'::jsonb),'presence',v_presence);
exception when unique_violation then
  return jsonb_build_object('ok',false,'error','room_exists');
end;
$$;

create or replace function public.bowling_room_pull(
  p_room_code text,
  p_pin text
) returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  r public.bowling_sync_rooms%rowtype;
  v_hash text := encode(digest(trim(coalesce(p_pin,'')),'sha256'),'hex');
begin
  select * into r
  from public.bowling_sync_rooms
  where room_code=upper(trim(coalesce(p_room_code,''))) and pin_hash=v_hash;
  if not found then
    return jsonb_build_object('ok',false,'error','not_found_or_pin');
  end if;
  return jsonb_build_object(
    'ok',true,
    'revision',r.revision,
    'payload',r.payload,
    'presence',r.presence,
    'updated_at',r.updated_at,
    'updated_by',r.updated_by
  );
end;
$$;

create or replace function public.bowling_room_touch(
  p_room_code text,
  p_pin text,
  p_device_id text,
  p_device_name text,
  p_role text
) returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  r public.bowling_sync_rooms%rowtype;
  v_hash text := encode(digest(trim(coalesce(p_pin,'')),'sha256'),'hex');
  v_role text := case when p_role in ('host','editor','viewer') then p_role else 'viewer' end;
  v_entry jsonb;
begin
  select * into r from public.bowling_sync_rooms
  where room_code=upper(trim(coalesce(p_room_code,''))) and pin_hash=v_hash
  for update;
  if not found then
    return jsonb_build_object('ok',false,'error','not_found_or_pin');
  end if;
  v_entry := jsonb_build_object(
    'deviceId',coalesce(nullif(p_device_id,''),'unknown'),
    'name',coalesce(nullif(p_device_name,''),'裝置'),
    'role',v_role,
    'lastSeen',(extract(epoch from clock_timestamp())*1000)::bigint
  );
  update public.bowling_sync_rooms
  set presence=jsonb_set(coalesce(presence,'{}'::jsonb),array[coalesce(nullif(p_device_id,''),'unknown')],v_entry,true)
  where room_code=r.room_code
  returning presence into r.presence;
  return jsonb_build_object('ok',true,'revision',r.revision,'presence',r.presence);
end;
$$;

create or replace function public.bowling_room_push(
  p_room_code text,
  p_pin text,
  p_payload jsonb,
  p_base_revision bigint,
  p_device_id text,
  p_device_name text,
  p_role text
) returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  r public.bowling_sync_rooms%rowtype;
  v_hash text := encode(digest(trim(coalesce(p_pin,'')),'sha256'),'hex');
  v_role text := case when p_role in ('host','editor') then p_role else 'viewer' end;
  v_entry jsonb;
begin
  if v_role='viewer' then
    return jsonb_build_object('ok',false,'error','viewer_cannot_push');
  end if;
  select * into r from public.bowling_sync_rooms
  where room_code=upper(trim(coalesce(p_room_code,''))) and pin_hash=v_hash
  for update;
  if not found then
    return jsonb_build_object('ok',false,'error','not_found_or_pin');
  end if;
  if coalesce(p_base_revision,0) <> r.revision then
    return jsonb_build_object('ok',false,'conflict',true,'revision',r.revision,'payload',r.payload,'presence',r.presence);
  end if;
  v_entry := jsonb_build_object(
    'deviceId',coalesce(nullif(p_device_id,''),'unknown'),
    'name',coalesce(nullif(p_device_name,''),'裝置'),
    'role',v_role,
    'lastSeen',(extract(epoch from clock_timestamp())*1000)::bigint
  );
  update public.bowling_sync_rooms
  set payload=coalesce(p_payload,'{}'::jsonb),
      revision=revision+1,
      updated_at=now(),
      updated_by=coalesce(p_device_id,''),
      presence=jsonb_set(coalesce(presence,'{}'::jsonb),array[coalesce(nullif(p_device_id,''),'unknown')],v_entry,true)
  where room_code=r.room_code
  returning * into r;
  return jsonb_build_object('ok',true,'revision',r.revision,'payload',r.payload,'presence',r.presence,'updated_at',r.updated_at);
end;
$$;

revoke all on function public.bowling_room_create(text,text,jsonb,text,text) from public;
revoke all on function public.bowling_room_pull(text,text) from public;
revoke all on function public.bowling_room_touch(text,text,text,text,text) from public;
revoke all on function public.bowling_room_push(text,text,jsonb,bigint,text,text,text) from public;

grant execute on function public.bowling_room_create(text,text,jsonb,text,text) to anon, authenticated;
grant execute on function public.bowling_room_pull(text,text) to anon, authenticated;
grant execute on function public.bowling_room_touch(text,text,text,text,text) to anon, authenticated;
grant execute on function public.bowling_room_push(text,text,jsonb,bigint,text,text,text) to anon, authenticated;

-- v0.4.1 Player Claim & Personal Score Sync

create table if not exists public.bowling_player_profiles (
  player_id text primary key,
  pin_hash text not null,
  display_name text not null default '',
  payload jsonb not null default '{}'::jsonb,
  revision bigint not null default 1,
  updated_at timestamptz not null default now(),
  updated_by text not null default ''
);

alter table public.bowling_player_profiles enable row level security;
revoke all on table public.bowling_player_profiles from anon, authenticated;

create or replace function public.bowling_player_create(
  p_player_id text,
  p_pin text,
  p_display_name text,
  p_payload jsonb,
  p_device_id text,
  p_device_name text
) returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  v_id text := upper(trim(coalesce(p_player_id,'')));
  v_pin text := trim(coalesce(p_pin,''));
  v_hash text;
begin
  if v_id !~ '^BM-[A-Z2-9]{6}$' then return jsonb_build_object('ok',false,'error','invalid_player_id'); end if;
  if v_pin !~ '^[0-9]{6}$' then return jsonb_build_object('ok',false,'error','invalid_pin'); end if;
  if exists(select 1 from public.bowling_player_profiles where player_id=v_id) then return jsonb_build_object('ok',false,'error','player_exists'); end if;
  v_hash := encode(digest(v_pin,'sha256'),'hex');
  insert into public.bowling_player_profiles(player_id,pin_hash,display_name,payload,revision,updated_at,updated_by)
  values(v_id,v_hash,left(coalesce(p_display_name,''),60),coalesce(p_payload,'{}'::jsonb),1,now(),coalesce(p_device_id,''));
  return jsonb_build_object('ok',true,'revision',1,'player_id',v_id,'display_name',left(coalesce(p_display_name,''),60),'payload',coalesce(p_payload,'{}'::jsonb));
exception when unique_violation then
  return jsonb_build_object('ok',false,'error','player_exists');
end;
$$;

create or replace function public.bowling_player_pull(
  p_player_id text,
  p_pin text
) returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  r public.bowling_player_profiles%rowtype;
  v_hash text := encode(digest(trim(coalesce(p_pin,'')),'sha256'),'hex');
begin
  select * into r from public.bowling_player_profiles
  where player_id=upper(trim(coalesce(p_player_id,''))) and pin_hash=v_hash;
  if not found then return jsonb_build_object('ok',false,'error','not_found_or_pin'); end if;
  return jsonb_build_object('ok',true,'revision',r.revision,'player_id',r.player_id,'display_name',r.display_name,'payload',r.payload,'updated_at',r.updated_at,'updated_by',r.updated_by);
end;
$$;

create or replace function public.bowling_player_push(
  p_player_id text,
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
  r public.bowling_player_profiles%rowtype;
  v_hash text := encode(digest(trim(coalesce(p_pin,'')),'sha256'),'hex');
  v_name text;
begin
  select * into r from public.bowling_player_profiles
  where player_id=upper(trim(coalesce(p_player_id,''))) and pin_hash=v_hash
  for update;
  if not found then return jsonb_build_object('ok',false,'error','not_found_or_pin'); end if;
  if coalesce(p_base_revision,0) <> r.revision then
    return jsonb_build_object('ok',false,'conflict',true,'revision',r.revision,'payload',r.payload,'display_name',r.display_name);
  end if;
  v_name := left(coalesce(nullif(p_payload #>> '{profile,displayName}',''),r.display_name),60);
  update public.bowling_player_profiles
  set payload=coalesce(p_payload,'{}'::jsonb),display_name=v_name,revision=revision+1,updated_at=now(),updated_by=coalesce(p_device_id,'')
  where player_id=r.player_id returning * into r;
  return jsonb_build_object('ok',true,'revision',r.revision,'player_id',r.player_id,'display_name',r.display_name,'payload',r.payload,'updated_at',r.updated_at);
end;
$$;

revoke all on function public.bowling_player_create(text,text,text,jsonb,text,text) from public;
revoke all on function public.bowling_player_pull(text,text) from public;
revoke all on function public.bowling_player_push(text,text,jsonb,bigint,text,text) from public;
grant execute on function public.bowling_player_create(text,text,text,jsonb,text,text) to anon, authenticated;
grant execute on function public.bowling_player_pull(text,text) to anon, authenticated;
grant execute on function public.bowling_player_push(text,text,jsonb,bigint,text,text) to anon, authenticated;

-- v0.4.2-R3 Personal PIN Change
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
  where player_id=upper(trim(coalesce(p_player_id,'')))
    and pin_hash=v_current_hash
  for update;

  if not found then
    return jsonb_build_object('ok',false,'error','not_found_or_pin');
  end if;

  v_new_hash := encode(digest(v_new_pin,'sha256'),'hex');

  update public.bowling_player_profiles
  set pin_hash=v_new_hash,
      revision=revision+1,
      updated_at=now(),
      updated_by=coalesce(p_device_id,'')
  where player_id=r.player_id
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

-- v0.4.2 Group History & Shared Records
-- Group Code + PIN allows members to read the group's complete shared history.
-- This is lightweight shared access, not account-grade authentication.

create table if not exists public.bowling_groups (
  group_code text primary key,
  pin_hash text not null,
  group_name text not null default 'BowlMeet Group',
  payload jsonb not null default '{}'::jsonb,
  revision bigint not null default 1,
  updated_at timestamptz not null default now(),
  updated_by text not null default ''
);

alter table public.bowling_groups enable row level security;
revoke all on table public.bowling_groups from anon, authenticated;

create or replace function public.bowling_group_create(
  p_group_code text,
  p_pin text,
  p_group_name text,
  p_payload jsonb,
  p_device_id text,
  p_device_name text
) returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  v_code text := upper(trim(coalesce(p_group_code,'')));
  v_pin text := trim(coalesce(p_pin,''));
  v_name text := left(trim(coalesce(p_group_name,'BowlMeet Group')),80);
  v_hash text;
begin
  if v_code !~ '^[A-Z2-9]{6}$' then
    return jsonb_build_object('ok',false,'error','invalid_group_code');
  end if;
  if v_pin !~ '^[0-9]{6}$' then
    return jsonb_build_object('ok',false,'error','invalid_pin');
  end if;
  if exists(select 1 from public.bowling_groups where group_code=v_code) then
    return jsonb_build_object('ok',false,'error','group_exists');
  end if;
  v_hash := encode(digest(v_pin,'sha256'),'hex');
  insert into public.bowling_groups(group_code,pin_hash,group_name,payload,revision,updated_at,updated_by)
  values(v_code,v_hash,coalesce(nullif(v_name,''),'BowlMeet Group'),coalesce(p_payload,'{}'::jsonb),1,now(),coalesce(p_device_id,''));
  return jsonb_build_object(
    'ok',true,
    'revision',1,
    'group_code',v_code,
    'group_name',coalesce(nullif(v_name,''),'BowlMeet Group'),
    'payload',coalesce(p_payload,'{}'::jsonb),
    'updated_at',now()
  );
exception when unique_violation then
  return jsonb_build_object('ok',false,'error','group_exists');
end;
$$;

create or replace function public.bowling_group_pull(
  p_group_code text,
  p_pin text
) returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  r public.bowling_groups%rowtype;
  v_hash text := encode(digest(trim(coalesce(p_pin,'')),'sha256'),'hex');
begin
  select * into r
  from public.bowling_groups
  where group_code=upper(trim(coalesce(p_group_code,''))) and pin_hash=v_hash;
  if not found then
    return jsonb_build_object('ok',false,'error','not_found_or_pin');
  end if;
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
  v_name := left(coalesce(nullif(p_payload #>> '{groupName}',''),r.group_name),80);
  update public.bowling_groups
  set payload=coalesce(p_payload,'{}'::jsonb),
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

revoke all on function public.bowling_group_create(text,text,text,jsonb,text,text) from public;
revoke all on function public.bowling_group_pull(text,text) from public;
revoke all on function public.bowling_group_push(text,text,jsonb,bigint,text,text) from public;

grant execute on function public.bowling_group_create(text,text,text,jsonb,text,text) to anon, authenticated;
grant execute on function public.bowling_group_pull(text,text) to anon, authenticated;
grant execute on function public.bowling_group_push(text,text,jsonb,bigint,text,text) to anon, authenticated;
 then
    return jsonb_build_object('ok',false,'error','invalid_new_pin');
  end if;
  if trim(coalesce(p_current_pin,'')) = v_new_pin then
    return jsonb_build_object('ok',false,'error','same_pin');
  end if;

  select * into r
  from public.bowling_player_profiles
  where player_id=upper(trim(coalesce(p_player_id,'')))
    and pin_hash=v_current_hash
  for update;

  if not found then
    return jsonb_build_object('ok',false,'error','not_found_or_pin');
  end if;

  v_new_hash := encode(digest(v_new_pin,'sha256'),'hex');

  update public.bowling_player_profiles
  set pin_hash=v_new_hash,
      revision=revision+1,
      updated_at=now(),
      updated_by=coalesce(p_device_id,'')
  where player_id=r.player_id
  returning * into r;

  return jsonb_build_object(
    'ok',true,
    'revision',r.revision,
    'player_id',r.player_id,
    'display_name',r.display_name,
    'updated_at',r.updated_at
  );
end;
$;

revoke all on function public.bowling_player_change_pin(text,text,text,text,text) from public;
grant execute on function public.bowling_player_change_pin(text,text,text,text,text) to anon, authenticated;



-- v0.4.2 Group History & Shared Records
-- Group Code + PIN allows members to read the group's complete shared history.
-- This is lightweight shared access, not account-grade authentication.

create table if not exists public.bowling_groups (
  group_code text primary key,
  pin_hash text not null,
  group_name text not null default 'BowlMeet Group',
  payload jsonb not null default '{}'::jsonb,
  revision bigint not null default 1,
  updated_at timestamptz not null default now(),
  updated_by text not null default ''
);

alter table public.bowling_groups enable row level security;
revoke all on table public.bowling_groups from anon, authenticated;

create or replace function public.bowling_group_create(
  p_group_code text,
  p_pin text,
  p_group_name text,
  p_payload jsonb,
  p_device_id text,
  p_device_name text
) returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  v_code text := upper(trim(coalesce(p_group_code,'')));
  v_pin text := trim(coalesce(p_pin,''));
  v_name text := left(trim(coalesce(p_group_name,'BowlMeet Group')),80);
  v_hash text;
begin
  if v_code !~ '^[A-Z2-9]{6}$' then
    return jsonb_build_object('ok',false,'error','invalid_group_code');
  end if;
  if v_pin !~ '^[0-9]{6}$' then
    return jsonb_build_object('ok',false,'error','invalid_pin');
  end if;
  if exists(select 1 from public.bowling_groups where group_code=v_code) then
    return jsonb_build_object('ok',false,'error','group_exists');
  end if;
  v_hash := encode(digest(v_pin,'sha256'),'hex');
  insert into public.bowling_groups(group_code,pin_hash,group_name,payload,revision,updated_at,updated_by)
  values(v_code,v_hash,coalesce(nullif(v_name,''),'BowlMeet Group'),coalesce(p_payload,'{}'::jsonb),1,now(),coalesce(p_device_id,''));
  return jsonb_build_object(
    'ok',true,
    'revision',1,
    'group_code',v_code,
    'group_name',coalesce(nullif(v_name,''),'BowlMeet Group'),
    'payload',coalesce(p_payload,'{}'::jsonb),
    'updated_at',now()
  );
exception when unique_violation then
  return jsonb_build_object('ok',false,'error','group_exists');
end;
$$;

create or replace function public.bowling_group_pull(
  p_group_code text,
  p_pin text
) returns jsonb
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  r public.bowling_groups%rowtype;
  v_hash text := encode(digest(trim(coalesce(p_pin,'')),'sha256'),'hex');
begin
  select * into r
  from public.bowling_groups
  where group_code=upper(trim(coalesce(p_group_code,''))) and pin_hash=v_hash;
  if not found then
    return jsonb_build_object('ok',false,'error','not_found_or_pin');
  end if;
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
  v_name := left(coalesce(nullif(p_payload #>> '{groupName}',''),r.group_name),80);
  update public.bowling_groups
  set payload=coalesce(p_payload,'{}'::jsonb),
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

revoke all on function public.bowling_group_create(text,text,text,jsonb,text,text) from public;
revoke all on function public.bowling_group_pull(text,text) from public;
revoke all on function public.bowling_group_push(text,text,jsonb,bigint,text,text) from public;

grant execute on function public.bowling_group_create(text,text,text,jsonb,text,text) to anon, authenticated;
grant execute on function public.bowling_group_pull(text,text) to anon, authenticated;
grant execute on function public.bowling_group_push(text,text,jsonb,bigint,text,text) to anon, authenticated;
