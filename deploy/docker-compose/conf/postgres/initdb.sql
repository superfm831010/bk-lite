DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'system_mgmt') THEN
        CREATE DATABASE system_mgmt;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'node_mgmt') THEN
        CREATE DATABASE node_mgmt;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'monitor') THEN
        CREATE DATABASE monitor;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ops-console') THEN
        CREATE DATABASE "ops-console";
    END IF;
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'cmdb') THEN
        CREATE DATABASE cmdb;
    END IF;
END
$$;