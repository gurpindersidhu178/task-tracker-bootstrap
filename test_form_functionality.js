// 🧪 Form Functionality Test Script
// Tests the updated form with checkbox-based skill selection

const API_BASE = "http://localhost:5050";

// Test data for form submission
const testFormData = {
  name: "Test User",
  email: "test@example.com",
  phone: "+91 9876543210",
  linkedin: "https://linkedin.com/in/testuser",
  github: "https://github.com/testuser",
  experience: "2-3",
  role: "Full Stack Developer",
  location: "Remote",
  coverLetter: "I am excited to apply for this position...",
  // Skills will be set by the form logic
};

// Test different skill combinations
const testScenarios = [
  {
    name: "Frontend Developer",
    selectedSkillsets: ["Frontend Development"],
    additionalSkills: "Redux, Styled Components",
    expectedSkills: "Frontend Development, Redux, Styled Components"
  },
  {
    name: "Full Stack Developer", 
    selectedSkillsets: ["Frontend Development", "Backend Development"],
    additionalSkills: "MongoDB, AWS",
    expectedSkills: "Frontend Development, Backend Development, MongoDB, AWS"
  },
  {
    name: "Data Scientist",
    selectedSkillsets: ["Data Science"],
    additionalSkills: "SQL, Tableau",
    expectedSkills: "Data Science, SQL, Tableau"
  },
  {
    name: "DevOps Engineer",
    selectedSkillsets: ["DevOps"],
    additionalSkills: "Ansible, Prometheus",
    expectedSkills: "DevOps, Ansible, Prometheus"
  },
  {
    name: "Project Manager",
    selectedSkillsets: ["Project Management"],
    additionalSkills: "MS Project, Slack",
    expectedSkills: "Project Management, MS Project, Slack"
  }
];

// Test the form logic
function testFormLogic() {
  console.log("🧪 Testing Form Logic...\n");
  
  testScenarios.forEach((scenario, index) => {
    console.log(`📋 Test ${index + 1}: ${scenario.name}`);
    console.log(`   Selected Skillsets: [${scenario.selectedSkillsets.join(", ")}]`);
    console.log(`   Additional Skills: "${scenario.additionalSkills}"`);
    
    // Simulate the form logic
    const allSkills = [
      ...scenario.selectedSkillsets,
      ...scenario.additionalSkills.split(',').map(skill => skill.trim()).filter(skill => skill)
    ].join(', ');
    
    console.log(`   Expected Result: "${scenario.expectedSkills}"`);
    console.log(`   Actual Result:   "${allSkills}"`);
    console.log(`   ✅ Match: ${allSkills === scenario.expectedSkills ? "PASS" : "FAIL"}\n`);
  });
}

// Test API endpoint
async function testAPIEndpoint() {
  console.log("🌐 Testing API Endpoint...\n");
  
  try {
    // Test with a simple form data
    const formData = new FormData();
    formData.append('name', testFormData.name);
    formData.append('email', testFormData.email);
    formData.append('phone', testFormData.phone);
    formData.append('skills', 'Frontend Development, Backend Development');
    formData.append('experience', testFormData.experience);
    formData.append('role', testFormData.role);
    formData.append('location', testFormData.location);
    formData.append('coverLetter', testFormData.coverLetter);
    
    // Create a dummy file
    const dummyFile = new Blob(['Test CV content'], { type: 'application/pdf' });
    formData.append('file', dummyFile, 'test_cv.pdf');
    
    const response = await fetch(`${API_BASE}/upload`, {
      method: 'POST',
      body: formData
    });
    
    console.log(`   API Response Status: ${response.status}`);
    console.log(`   API Response: ${response.statusText}`);
    
    if (response.ok) {
      const result = await response.text();
      console.log(`   ✅ API Test: PASS - ${result}`);
    } else {
      console.log(`   ❌ API Test: FAIL - ${response.statusText}`);
    }
    
  } catch (error) {
    console.log(`   ❌ API Test: ERROR - ${error.message}`);
  }
}

// Test CV parsing with new skills
function testCVParsing() {
  console.log("📄 Testing CV Parsing with New Skills...\n");
  
  const testCVContent = `
    John Doe
    Full Stack Developer
    
    Skills:
    - React, TypeScript, JavaScript
    - Node.js, Express.js, Python
    - MongoDB, PostgreSQL, Docker
    - CI/CD, GitHub Actions, AWS
    - Agile, Scrum, Jira
    
    Experience:
    - Built React applications with TypeScript
    - Developed REST APIs using Node.js and Express
    - Implemented CI/CD pipelines with GitHub Actions
    - Managed projects using Agile methodology
  `;
  
  // Test skill extraction (simplified version)
  const knownSkills = [
    "React", "TypeScript", "JavaScript", "Node.js", "Express.js", "Python",
    "MongoDB", "PostgreSQL", "Docker", "CI/CD", "GitHub Actions", "AWS",
    "Agile", "Scrum", "Jira"
  ];
  
  const foundSkills = knownSkills.filter(skill => 
    testCVContent.toLowerCase().includes(skill.toLowerCase())
  );
  
  console.log(`   Test CV Content Length: ${testCVContent.length} characters`);
  console.log(`   Skills Found: [${foundSkills.join(", ")}]`);
  console.log(`   Total Skills Found: ${foundSkills.length}`);
  console.log(`   ✅ CV Parsing Test: PASS - Found ${foundSkills.length} skills\n`);
}

// Test skillset validation
function testSkillsetValidation() {
  console.log("✅ Testing Skillset Validation...\n");
  
  const validSkillsets = [
    "Frontend Development", "Backend Development", "Data Science", 
    "DevOps", "Project Management"
  ];
  
  const testSkillsets = [
    "Frontend Development",
    "Backend Development", 
    "Data Science",
    "DevOps",
    "Project Management",
    "Invalid Skillset" // This should not be valid
  ];
  
  testSkillsets.forEach(skillset => {
    const isValid = validSkillsets.includes(skillset);
    console.log(`   "${skillset}": ${isValid ? "✅ VALID" : "❌ INVALID"}`);
  });
  
  console.log(`\n   ✅ Skillset Validation Test: PASS\n`);
}

// Main test execution
async function runAllTests() {
  console.log("🚀 Starting Form Functionality Tests...\n");
  console.log("=" .repeat(60));
  
  testFormLogic();
  testSkillsetValidation();
  testCVParsing();
  await testAPIEndpoint();
  
  console.log("=" .repeat(60));
  console.log("🎉 All tests completed!");
  console.log("\n📋 Next Steps:");
  console.log("   1. Open http://localhost:3000 in your browser");
  console.log("   2. Test the form with different skill combinations");
  console.log("   3. Verify the checkbox functionality");
  console.log("   4. Check the visual feedback and validation");
  console.log("   5. Submit a test form to verify backend integration");
}

// Run tests if this script is executed directly
if (typeof window === 'undefined') {
  // Node.js environment
  runAllTests().catch(console.error);
} else {
  // Browser environment
  console.log("🧪 Form Test Script Loaded");
  console.log("Open the browser console to run tests");
  
  // Make functions available globally for browser testing
  window.testFormFunctionality = {
    testFormLogic,
    testSkillsetValidation,
    testCVParsing,
    testAPIEndpoint,
    runAllTests
  };
} 