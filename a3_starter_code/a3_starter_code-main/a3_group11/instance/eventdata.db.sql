BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "events" (
	"id"	INTEGER NOT NULL,
	"event_name"	VARCHAR(100) NOT NULL,
	"event_category"	VARCHAR(20) NOT NULL,
	"event_thumbnail"	VARCHAR(400) NOT NULL,
	"event_summary"	VARCHAR(200) NOT NULL,
	"event_location"	VARCHAR(200) NOT NULL,
	"event_type"	VARCHAR(200) NOT NULL,
	"start_date"	DATE NOT NULL,
	"end_date"	DATE NOT NULL,
	"event_description"	VARCHAR(400) NOT NULL,
	"start_time"	VARCHAR(20) NOT NULL,
	"end_time"	VARCHAR(20) NOT NULL,
	"ticket_price"	INTEGER NOT NULL,
	"ticket_quantity"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"full_name"	VARCHAR(100) NOT NULL,
	"contact_number"	INTEGER NOT NULL,
	"email_id"	VARCHAR(100) NOT NULL,
	"address"	VARCHAR(100) NOT NULL,
	"password_hash"	VARCHAR(400) NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "comments" (
	"id"	INTEGER NOT NULL,
	"text"	VARCHAR(400) NOT NULL,
	"posted_at"	DATETIME NOT NULL,
	"event_id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id"),
	FOREIGN KEY("event_id") REFERENCES "events"("id")
);
CREATE TABLE IF NOT EXISTS "booking_statuses" (
	"id"	INTEGER NOT NULL,
	"status"	VARCHAR(50) NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "bookings" (
	"id"	INTEGER NOT NULL,
	"event_name"	VARCHAR(100) NOT NULL,
	"event_price"	FLOAT NOT NULL,
	"event_quantity"	INTEGER NOT NULL,
	"event_date"	DATETIME NOT NULL,
	"start_time"	VARCHAR(20) NOT NULL,
	"end_time"	VARCHAR(20) NOT NULL,
	"event_location"	VARCHAR(200) NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"event_id"	INTEGER NOT NULL,
	"status_id"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("event_id") REFERENCES "events"("id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id"),
	FOREIGN KEY("status_id") REFERENCES "booking_statuses"("id")
);
CREATE UNIQUE INDEX IF NOT EXISTS "ix_user_address" ON "users" (
	"address"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ix_user_full_name" ON "users" (
	"full_name"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ix_user_email_id" ON "users" (
	"email_id"
);
COMMIT;
