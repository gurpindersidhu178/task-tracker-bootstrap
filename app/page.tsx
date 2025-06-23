'use client';

import { useState } from 'react';

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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, files } = e.target as any;
    setFormData((prev) => ({
      ...prev,
      [name]: files ? files[0] : value,
    }));
  };

  const handleSubmit = async () => {
    // Required fields
    if (!formData.name || !formData.email || !formData.skills || !formData.careerAspiration || !formData.resume) {
      setStatus('❗ Please fill in all required fields.');
      return;
    }
    const fd = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
      if (value && key !== 'resume') {
        fd.append(key, value as any);
      }
    });
    // Add the file with the correct field name that the backend expects
    if (formData.resume) {
      fd.append('file', formData.resume);
    }

    setStatus('📤 Uploading and processing your CV...');
    try {
      // Use environment variable for API URL with Railway production fallback
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
          setStatus('✅ CV submitted successfully. You will receive your assignment by email.');
        }
      } else {
        // Handle specific error messages from backend
        const errorMessage = data.error || 'Upload failed. Please try again.';
        setStatus(`❌ ${errorMessage}`);
      }
    } catch (error) {
      console.error('Upload error:', error);
      setStatus('❌ Network error. Please check your connection and try again.');
    }
  };

  return (
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