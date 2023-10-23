--Create forecast table to store daily site flow predictions
--site_id and ts are used as joint primary key

CREATE TABLE rr.forecast(
   site_id uuid,    
   ts timestamptz,  
   value numeric,
   PRIMARY KEY (site_id, ts)
);
