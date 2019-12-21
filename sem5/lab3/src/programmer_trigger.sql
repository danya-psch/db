create TABLE IF NOT EXISTS dead_programmers (
    id serial PRIMARY KEY,
    name text NOT NULL
);

truncate dead_programmers RESTART IDENTITY;
create or replace function programmer_trigger() returns trigger
as $$
declare
    new_description text;
    current_name text;
begin
    if new is not null then
        new_description = ((SELECT description FROM developer_company WHERE id = new.developer_company_id) || '!');
        UPDATE developer_company SET description = new_description WHERE id = new.developer_company_id;
        for current_name in SELECT name FROM dead_programmers loop
            if new.name like current_name then
                raise '% is already dead', current_name;
            end if;
        end loop;
    else
        INSERT INTO dead_programmers (name)
            VALUES (old.name);
        return old;
    end if;
    return new;
    exception
        when no_data_found then
        when too_many_rows then
            raise 'Could not check description, try again later';
end;
$$ language plpgsql;

drop trigger IF EXISTS programmer_helper on programmer;
create trigger programmer_helper before delete or update on programmer for each row EXECUTE procedure programmer_trigger();