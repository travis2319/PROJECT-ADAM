<h1 align="center">PROJECT ADAM 🚗🔧</h1>

**PROJECT ADAM** is an automotive diagnostic and monitoring system that helps in logging engine health and making predictions about its performance.

## Environment

1. Create a `.env` file in the root directory
2. Add the following environment variables:

   ```plaintext
   EXPO_PUBLIC_SUPABASE_URL=your_supabase_project_url
   EXPO_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   DATABASE_URL=your_database_url
   DIRECT_URL=your_direct_url
   ```

## Setup

1. Install dependencies

   ```bash
   npm install
   ```

2. Push Prisma schema to the database

   ```bash
   npx prisma db push
   ```

3. Start the app

   ```bash
   npm start
   ```
