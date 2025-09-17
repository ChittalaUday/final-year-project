import { PrismaClient } from "../../generated/prisma/index.js";
const prisma = new PrismaClient();

export async function postgresConnection() {
  try {
    await prisma.$connect();
    console.log("🤝 Connected to 🐘 Postgress Successfully...");
  } catch (err) {
    console.error("❌ Connection Failed: ", err);
  } finally {
    await prisma.$disconnect();
  }
}

export default prisma;
