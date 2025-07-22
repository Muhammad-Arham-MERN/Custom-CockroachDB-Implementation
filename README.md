# OpenAI Agents SDK CockroachDB Session Implementation (Custom)

A plug-and-play session implementation using CockroachDB for OpenAI Agents SDK, suitable for production-level use.

Let's get you started, it is so easy as if started and finished are the *same thing* 😅

## Prerequisities
make sure following dependencies are installed on your project
- openai-agents
- sqlmodel

## Implementation Steps:
### CockroachDB Connection String

1. Visit CockroachDB
Go to: https://www.cockroachlabs.com/

2. Click "Get Started For Free"
Begin the sign-up process.

3. Sign Up
Choose your preferred credential provider (Google, GitHub, etc.) and select the "Basic Free" plan.

4. Choose Cloud Provider & Region
Pick a cloud that’s geographically closest to you (to reduce latency).

5. Keep Defaults & Add Payment Method
Leave capacity options as-is. Add a payment method (this is required but you’ll get a 1-month free trial).

6. Generate Username & Password
When prompted, generate your database username and password. Click "Next".

7. Install CA Certificates (One-time setup)
Install the CA Certificates by running the *mkdir* command as instructed in popup as well screenshot below

8. Select Language
Scroll to the language selection area and choose Python.

9. Select SQL Tool
Set the SQL tool to SQLAlchemy.

10. Copy Connection String
You’ll receive a connection string like this:
cockroachdb://username:REVEAL_PASSWORD@maroon-shaman-13575.j77.aws-ap-southeast-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full
<img width="481" height="654" alt="d" src="https://github.com/user-attachments/assets/ddc1fe85-5d35-459e-aa81-93035ca0bd18" />

11. Done ✅
Copy this connection string — you’ll use it in your code. That’s it!

### Final Steps (Befre continuing i am assuming you have the knowledge of what env variables are!)
1. Yes the only thing you need is that connection string associated with a cloud based DB
2. Now store that connection string in an ENV variable named *COCKROACHDB_URL*
3. Download SQLImplementation.py file
4. You will see a 200+ lined code, your concern is this currently:
   ~~~python
   cockroachdb_connection_url = os.getenv("COCKROACHDB_URL").replace(
    "postgresql", "cockroachdb"
    )
   ~~~
   > I was having an issue that when importing my env variable, i always received postgresql in my connection uri instead of *cockroachdb*, Keep this in note that whenever you are using this Class, just make sure that the ENV Variable you are loading is exactly the connection string you took from the PostgreSQL Database Provider like (Neon db, cockroachdb etc), If your env variables are imported without errors/unknown manipulations, you can remove that logic and just get os.getenv("COCKROACHDB_URL")
5. Open Example.py file it is exactly how you implement SQLlite Session just you are importing a custom session here
6. make an instance of CockroachDBSession (first make sure you import it in your agents file) and add an argument of *session_id* (very important)
7. That is it!

