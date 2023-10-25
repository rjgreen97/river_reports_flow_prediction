# RiverReports Flow Predictions

![alt text](https://flyrods.weebly.com/uploads/2/9/0/8/2908219/8020826_orig.jpg)

## Order of Operations
1) Use code found in **forecasting.sql** to create a `forecast` table
2) Create a `.env` file and set the database URL to the `DATABASE_URL` key in the following format: 
    * `postgres://[user]:[pass]@[host]:[port]/[db]`
3) run `bin/forecasting_session` which will create a **ForcastingSession** object, creating forecasts for all sites and write 7-day predictions to the `forecast` table
