create table pusers(
  uid UUID default gen_random_uuid() PRIMARY KEY,
  name text not null,
  email text not null
)
-- console: http://10.10.1.200:8081/
-- access: postgres://postgres:postgres@10.10.1.200:5432/postgres