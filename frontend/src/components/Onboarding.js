import React, { useState } from 'react';

const Onboarding = ({ isOpen, onClose }) => {
  const [step, setStep] = useState(0);
  
  const steps = [
    {
      title: 'Welcome to Hazel 1.0',
      description: 'Your AI-powered legal document assistant',
      image: '/onboarding/welcome.svg'
    },
    {
      title: 'Upload Documents',
      description: 'Upload legal documents, contracts, or case files for analysis',
      image: '/onboarding/upload.svg'
    },
    {
      title: 'Ask Questions',
      description: 'Ask specific questions about your documents or legal matters',
      image: '/onboarding/ask.svg'
    },
    {
      title: 'Generate Documents',
      description: 'Generate legal documents based on your requirements',
      image: '/onboarding/generate.svg'
    }
  ];
  
  if (!isOpen) return null;
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-medium text-secondary-900">{steps[step].title}</h2>
          <button onClick={onClose} className="text-secondary-500 hover:text-secondary-700">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div className="mb-6 flex flex-col items-center">
          <img src={steps[step].image} alt={steps[step].title} className="w-64 h-64 mb-4" />
          <p className="text-center text-secondary-600">{steps[step].description}</p>
        </div>
        
        <div className="flex justify-between items-center">
          <button
            onClick={() => setStep(prev => Math.max(0, prev - 1))}
            disabled={step === 0}
            className="px-4 py-2 border border-secondary-300 text-sm font-medium rounded-md text-secondary-700 bg-white hover:bg-secondary-50 disabled:opacity-50"
          >
            Previous
          </button>
          
          <div className="flex space-x-1">
            {steps.map((_, i) => (
              <div
                key={i}
                className={`w-2 h-2 rounded-full ${i === step ? 'bg-primary-600' : 'bg-secondary-300'}`}
              />
            ))}
          </div>
          
          {step < steps.length - 1 ? (
            <button
              onClick={() => setStep(prev => Math.min(steps.length - 1, prev + 1))}
              className="px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-700 hover:bg-primary-800"
            >
              Next
            </button>
          ) : (
            <button
              onClick={onClose}
              className="px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-700 hover:bg-primary-800"
            >
              Get Started
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default Onboarding; 