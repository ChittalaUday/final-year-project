import { PrismaClient as PostgresClient } from "@prisma/client-postgres";
import { PrismaClient as MongoClient } from "@prisma/client-mongodb";

declare global {
  var prismaPostgres: PostgresClient | undefined;
  var prismaMongo: MongoClient | undefined;
}

const prismaPostgres =
  global.prismaPostgres ||
  new PostgresClient({
    log: ["query", "info", "warn", "error"],
  });

const prismaMongo =
  global.prismaMongo ||
  new MongoClient({
    log: ["info", "warn", "error"],
  });

if (process.env.NODE_ENV !== "production") {
  global.prismaPostgres = prismaPostgres;
  global.prismaMongo = prismaMongo;
}

export const postgres = prismaPostgres;
export const mongo = prismaMongo;

export async function postgresConnection() {
  try {
    await prismaPostgres.$connect();
    console.log("✅ PostgreSQL Connected successfully");
  } catch (error) {
    console.error("❌ PostgreSQL Connection failed:", error);
    process.exit(1);
  }
}

export default {
  postgres,
  mongo,
};
