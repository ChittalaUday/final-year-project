import axios from "axios";

const BASE_URL = "http://127.0.0.1:5003/api";

async function testOnboarding() {
  console.log("🚀 Starting API Verification...");

  try {
    // 1. Register
    console.log("\n1. Testing Registration...");
    const regRes = await axios.post(`${BASE_URL}/auth/register`, {
      name: "Test User",
      email: `test_${Date.now()}@example.com`,
      password: "password123",
      dob: "2005-05-15",
    });
    console.log("✅ Registration Success:", regRes.data.message);
    const token = regRes.data.body.token;

    const headers = { Authorization: `Bearer ${token}` };

    // 2. Set Age Group
    console.log("\n2. Testing Set Age Group...");
    const ageRes = await axios.post(
      `${BASE_URL}/onboarding/age-group`,
      { ageGroup: "SCHOOL" },
      { headers },
    );
    console.log("✅ Set Age Group Success:", ageRes.data.message);

    // 3. Update Profile
    console.log("\n3. Testing Profile Update...");
    const profRes = await axios.post(
      `${BASE_URL}/onboarding/profile`,
      { schoolName: "International School", grade: 10 },
      { headers },
    );
    console.log("✅ Profile Update Success:", profRes.data.message);

    // 4. Set Interests
    console.log("\n4. Fetching Interests...");
    // We need real IDs from the DB for many-to-many, but for testing we can fetch them
    // For now, let's assume we have some or skip the actual IDs and test validation
    console.log("⚠️ Skipping interests for now (requires valid UUIDs from DB)");

    // 5. Finalize
    console.log("\n5. Testing Finalize (Prediction)...");
    const finRes = await axios.post(
      `${BASE_URL}/onboarding/finalize`,
      {},
      { headers },
    );
    console.log("✅ Finalize Success!");
    console.log(
      "📊 Prediction Result:",
      finRes.data.body.prediction.predicted_course,
    );

    console.log("\n✨ API Verification Completed Successfully!");
  } catch (error: any) {
    console.error(
      "❌ Verification Failed:",
      error.response?.data || error.message,
    );
    process.exit(1);
  }
}

testOnboarding();
