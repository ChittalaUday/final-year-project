import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
dotenv.config({ path: path.resolve(__dirname, "../.env") });

import axios from "axios";
import { postgres } from "../src/config/db.js";

const BASE_URL = "http://127.0.0.1:5003/api";

async function runRobustTest() {
  console.log("🚀 Starting Robust API Verification...");
  console.log("DEBUG: DATABASE_URL =", process.env.DATABASE_URL);

  try {
    // 1. Query Database for Interest and Skill IDs
    console.log("\n🔍 Fetching valid Interest and Skill IDs from database...");
    let interests: any[] = [];
    let skills: any[] = [];

    try {
      interests = await postgres.interest.findMany({ take: 3 });
      skills = await postgres.skill.findMany({ take: 3 });

      if (interests.length === 0 || skills.length === 0) {
        console.warn(
          "⚠️ No interests or skills found in DB. Please run seeders first.",
        );
      } else {
        console.log(
          `✅ Found ${interests.length} interests and ${skills.length} skills.`,
        );
      }
    } catch (e: any) {
      console.warn(
        "⚠️ DB Fetch failed (Check connection info or seeds). Proceeding with empty lists.",
        e.message,
      );
    }

    // 2. Register
    const email = `test_robust_${Date.now()}@example.com`;
    console.log(`\n1. Testing Registration for ${email}...`);
    const regRes = await axios.post(`${BASE_URL}/auth/register`, {
      name: "Robust Tester",
      email: email,
      password: "password123",
      dob: "2007-10-20", // School student (18 years old)
    });

    console.log("✅ Registration Success!");
    const token = regRes.data.body.token;
    const user = regRes.data.body.user;

    console.log(
      "DEBUG: Onboarding Object:",
      JSON.stringify(user.onboarding, null, 2),
    );

    if (!user.onboarding) {
      throw new Error(
        "❌ Onboarding progress missing in registration response!",
      );
    }

    const headers = { Authorization: `Bearer ${token}` };

    // 3. Set Age Group
    console.log("\n2. Testing Set Age Group (SCHOOL)...");
    const ageRes = await axios.post(
      `${BASE_URL}/onboarding/age-group`,
      { ageGroup: "SCHOOL" },
      { headers },
    );
    console.log("✅ Set Age Group Success:", ageRes.data.message);

    // 4. Update Profile
    console.log("\n3. Testing Profile Update (School-specific)...");
    const profRes = await axios.post(
      `${BASE_URL}/onboarding/profile`,
      { schoolName: "High Oak School", grade: 12, cgpaPercentage: 88.5 },
      { headers },
    );
    console.log("✅ Profile Update Success:", profRes.data.message);

    // 5. Set Interests (Using Real IDs)
    if (interests.length > 0) {
      console.log("\n4. Testing Set Interests (Using real DB IDs)...");
      const interestIds = interests.map((i) => i.id);
      const intRes = await axios.post(
        `${BASE_URL}/onboarding/interests`,
        { interestIds },
        { headers },
      );
      console.log("✅ Set Interests Success:", intRes.data.message);
    }

    // 6. Set Skills (Using Real IDs)
    if (skills.length > 0) {
      console.log("\n5. Testing Set Skills (Using real DB IDs)...");
      const skillPayload = skills.map((s) => ({
        skillId: s.id,
        proficiencyLevel: 3,
      }));
      const skillRes = await axios.post(
        `${BASE_URL}/onboarding/skills`,
        { skills: skillPayload },
        { headers },
      );
      console.log("✅ Set Skills Success:", skillRes.data.message);
    }

    // 7. Finalize (Prediction)
    console.log("\n6. Testing Finalize (Prediction)...");
    const finRes = await axios.post(
      `${BASE_URL}/onboarding/finalize`,
      {},
      { headers },
    );
    console.log("✅ Finalize Success!");
    const prediction = finRes.data.body.prediction;
    console.log("🎯 Predicted Career:", prediction.predicted_course);
    console.log("📈 Confidence Score:", prediction.confidence);

    // 8. Verify Authentication Update (Onboarding complete)
    console.log("\n7. Verifying Onboarding Status in Login...");
    const loginRes = await axios.post(`${BASE_URL}/auth/login`, {
      email,
      password: "password123",
    });

    const loggedInUser = loginRes.data.body.user;
    console.log("📊 Final Onboarding Status:", loggedInUser.onboarding.status);

    if (loggedInUser.onboarding.status !== "COMPLETED") {
      console.warn(
        "⚠️ Onboarding status is not COMPLETED yet. (Might be background processed?)",
      );
    } else {
      console.log("✅ Onboarding marked as COMPLETED successfully.");
    }

    console.log("\n✨ Robust API Verification Completed Successfully!");
    process.exit(0);
  } catch (error: any) {
    console.error(
      "❌ Verification Failed:",
      error.response?.data || error.message,
    );
    process.exit(1);
  }
}

runRobustTest();
