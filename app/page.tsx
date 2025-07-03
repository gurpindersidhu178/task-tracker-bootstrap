'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';

export default function CareerPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    linkedin: '',
    github: '',
    skills: '',
    experience: '',
    role: '',
    location: '',
    coverLetter: '',
    careerAspiration: '',
    resume: null as File | null,
  });
  const [status, setStatus] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, files } = e.target as any;
    setFormData((prev) => ({
      ...prev,
      [name]: files ? files[0] : value,
    }));
  };

  const handleSubmit = async () => {
    if (!formData.name || !formData.email || !formData.skills || !formData.careerAspiration || !formData.resume) {
      setStatus('❗ Please fill in all required fields.');
      return;
    }

    setIsSubmitting(true);
    setStatus('📤 Uploading and processing your CV...');

    const fd = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
      if (value && key !== 'resume') {
        fd.append(key, value as any);
      }
    });
    if (formData.resume) {
      fd.append('file', formData.resume);
    }

    try {
      const API_BASE = process.env.NEXT_PUBLIC_API_URL || "https://logbiz-parse-api-production.up.railway.app";
      const res = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        body: fd,
      });

      const data = await res.json();

      if (res.ok) {
        if (data.warning) {
          setStatus(`✅ ${data.message} (${data.warning})`);
        } else {
          setStatus('✅ CV submitted successfully! You will receive your assignment by email within 24 hours.');
        }
      } else {
        const errorMessage = data.error || 'Upload failed. Please try again.';
        setStatus(`❌ ${errorMessage}`);
      }
    } catch (error) {
      console.error('Upload error:', error);
      setStatus('❌ Network error. Please check your connection and try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const nextStep = () => {
    if (currentStep < 3) setCurrentStep(currentStep + 1);
  };

  const prevStep = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-6 py-8">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
              CricoPro Platform
            </h1>
            <p className="text-xl text-gray-600 mb-2">Join Our Elite Development Team</p>
            <p className="text-gray-500">Paid Assignments • Real Projects • Career Growth</p>
          </motion.div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="max-w-4xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between mb-8">
          {[1, 2, 3].map((step) => (
            <div key={step} className="flex items-center">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold ${
                step <= currentStep 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-200 text-gray-500'
              }`}>
                {step}
              </div>
              {step < 3 && (
                <div className={`w-16 h-1 mx-2 ${
                  step < currentStep ? 'bg-blue-600' : 'bg-gray-200'
                }`} />
              )}
            </div>
          ))}
        </div>
        <div className="text-center mb-8">
          <h2 className="text-2xl font-semibold text-gray-800">
            {currentStep === 1 && 'Personal Information'}
            {currentStep === 2 && 'Skills & Experience'}
            {currentStep === 3 && 'Upload & Submit'}
          </h2>
        </div>
      </div>

      {/* Form Container */}
      <div className="max-w-2xl mx-auto px-6 pb-12">
        <motion.div
          key={currentStep}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
          className="bg-white rounded-2xl shadow-xl p-8"
        >
          {/* Step 1: Personal Information */}
          {currentStep === 1 && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Full Name *</label>
                <input
                  name="name"
                  type="text"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  placeholder="Enter your full name"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email Address *</label>
                <input
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  placeholder="your.email@example.com"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Phone Number</label>
                  <input
                    name="phone"
                    type="tel"
                    value={formData.phone}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="+1 (555) 123-4567"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
                  <input
                    name="location"
                    type="text"
                    value={formData.location}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="City, Country"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">LinkedIn Profile</label>
                  <input
                    name="linkedin"
                    type="url"
                    value={formData.linkedin}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="https://linkedin.com/in/yourprofile"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">GitHub/Portfolio</label>
                  <input
                    name="github"
                    type="url"
                    value={formData.github}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="https://github.com/yourusername"
                  />
                </div>
              </div>
            </div>
          )}

          {/* Step 2: Skills & Experience */}
          {currentStep === 2 && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Skills & Technologies *</label>
                <textarea
                  name="skills"
                  value={formData.skills}
                  onChange={handleChange}
                  rows={3}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  placeholder="e.g., React, Node.js, Python, AWS, Docker, TypeScript, MongoDB..."
                />
                <p className="text-sm text-gray-500 mt-1">List your technical skills, separated by commas</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Years of Experience</label>
                <select
                  name="experience"
                  value={formData.experience}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                >
                  <option value="">Select your experience level</option>
                  <option value="0-1">0-1 years (Fresher/Entry Level)</option>
                  <option value="2-3">2-3 years (Mid Level)</option>
                  <option value="4-5">4-5 years (Senior Level)</option>
                  <option value="6+">6+ years (Expert Level)</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Preferred Role</label>
                <input
                  name="role"
                  type="text"
                  value={formData.role}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  placeholder="e.g., Frontend Developer, Backend Engineer, Full Stack Developer"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Career Aspiration *</label>
                <textarea
                  name="careerAspiration"
                  value={formData.careerAspiration}
                  onChange={handleChange}
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  placeholder="Tell us about your career goals, what you want to achieve, and why you're interested in joining our team..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Cover Letter (Optional)</label>
                <textarea
                  name="coverLetter"
                  value={formData.coverLetter}
                  onChange={handleChange}
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  placeholder="Why should we consider you for this opportunity? What makes you stand out?"
                />
              </div>
            </div>
          )}

          {/* Step 3: Upload & Submit */}
          {currentStep === 3 && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Upload Your CV/Resume *</label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                  <input
                    name="resume"
                    type="file"
                    accept=".pdf,.doc,.docx"
                    onChange={handleChange}
                    className="hidden"
                    id="resume-upload"
                  />
                  <label htmlFor="resume-upload" className="cursor-pointer">
                    <div className="text-gray-600">
                      <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                      <p className="text-lg font-medium">Click to upload your CV</p>
                      <p className="text-sm">PDF, DOC, or DOCX (Max 10MB)</p>
                    </div>
                  </label>
                </div>
                {formData.resume && (
                  <div className="mt-2 p-3 bg-green-50 border border-green-200 rounded-lg">
                    <p className="text-sm text-green-700">✓ {formData.resume.name} selected</p>
                  </div>
                )}
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="font-medium text-blue-900 mb-2">What happens next?</h3>
                <ul className="text-sm text-blue-800 space-y-1">
                  <li>• We'll review your CV and skills</li>
                  <li>• You'll receive a personalized technical assignment</li>
                  <li>• Complete the assignment to proceed to interview</li>
                  <li>• Successful candidates join our paid project team</li>
                </ul>
              </div>
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="flex justify-between mt-8">
            {currentStep > 1 && (
              <button
                onClick={prevStep}
                className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                ← Previous
              </button>
            )}
            
            {currentStep < 3 ? (
              <button
                onClick={nextStep}
                className="ml-auto px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Next →
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={isSubmitting}
                className="ml-auto px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? 'Submitting...' : 'Submit Application'}
              </button>
            )}
          </div>

          {/* Status Message */}
          {status && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`mt-6 p-4 rounded-lg ${
                status.includes('✅') ? 'bg-green-50 border border-green-200 text-green-800' :
                status.includes('❌') ? 'bg-red-50 border border-red-200 text-red-800' :
                'bg-blue-50 border border-blue-200 text-blue-800'
              }`}
            >
              {status}
            </motion.div>
          )}
        </motion.div>
      </div>

      {/* Footer */}
      <div className="bg-gray-50 border-t mt-12">
        <div className="max-w-4xl mx-auto px-6 py-8 text-center">
          <p className="text-gray-600">© 2024 CricoPro Platform. All rights reserved.</p>
        </div>
      </div>
    </div>
  );
} 
    <div style={{ maxWidth: 650, margin: 'auto', padding: 20, fontFamily: 'Arial', fontSize: '16px' }}>
      <h1 style={{ fontSize: 28, fontWeight: 'bold', marginBottom: 24 }}>Submit Your CV</h1>
      <input name="name" type="text" value={formData.name} onChange={handleChange} placeholder="Full Name *" required style={{ display: 'block', width: '100%', marginBottom: 20, padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '4px' }} />
      <input name="email" type="email" value={formData.email} onChange={handleChange} placeholder="Email *" required style={{ display: 'block', width: '100%', marginBottom: 20, padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '4px' }} />
      <input name="phone" type="tel" value={formData.phone} onChange={handleChange} placeholder="Phone (Optional)" style={{ display: 'block', width: '100%', marginBottom: 20, padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '4px' }} />
      <input name="linkedin" type="url" value={formData.linkedin} onChange={handleChange} placeholder="LinkedIn Profile (Optional)" style={{ display: 'block', width: '100%', marginBottom: 20, padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '4px' }} />
      <input name="github" type="url" value={formData.github} onChange={handleChange} placeholder="GitHub / Portfolio (Optional)" style={{ display: 'block', width: '100%', marginBottom: 20, padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '4px' }} />
      <input name="skills" type="text" value={formData.skills} onChange={handleChange} placeholder="Skills (comma separated) *" required style={{ display: 'block', width: '100%', marginBottom: 20, padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '4px' }} />
      <select name="experience" value={formData.experience} onChange={handleChange} style={{ display: 'block', width: '100%', marginBottom: 20, padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '4px' }}>
        <option value="">Years of Experience (Select)</option>
        <option value="0-1">0-1</option>
        <option value="2-3">2-3</option>
        <option value="4-5">4-5</option>
        <option value="6+">6+</option>
      </select>
      <input name="role" type="text" value={formData.role} onChange={handleChange} placeholder="Preferred Role (Optional)" style={{ display: 'block', width: '100%', marginBottom: 20, padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '4px' }} />
      <input name="location" type="text" value={formData.location} onChange={handleChange} placeholder="Location Preference (Optional)" style={{ display: 'block', width: '100%', marginBottom: 20, padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '4px' }} />
      <textarea name="careerAspiration" value={formData.careerAspiration} onChange={handleChange} placeholder="Career Aspiration *" required rows={3} style={{ display: 'block', width: '100%', marginBottom: 20, padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '4px' }} />
      <textarea name="coverLetter" value={formData.coverLetter} onChange={handleChange} placeholder="Cover Letter (Optional)" rows={4} style={{ display: 'block', width: '100%', marginBottom: 20, padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '4px' }} />
      <input name="resume" type="file" accept=".pdf,.doc,.docx" onChange={handleChange} required style={{ marginBottom: 20, fontSize: '16px' }} />
      <button onClick={handleSubmit} style={{ padding: '12px 24px', fontSize: '16px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Submit</button>
      <p style={{ marginTop: 20, fontSize: '16px' }}>{status}</p>
    </div>
  );
} 