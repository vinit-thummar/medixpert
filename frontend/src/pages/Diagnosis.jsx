import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useAuth } from '../contexts/AuthContext';
import { 
  Brain, 
  Search, 
  Plus, 
  X, 
  AlertCircle, 
  CheckCircle, 
  Loader2,
  TrendingUp,
  Activity,
  Calendar,
  FileText
} from 'lucide-react';

const Diagnosis = () => {
  const { user } = useAuth();
  const [symptoms, setSymptoms] = useState([]);
  const [symptomInput, setSymptomInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [availableSymptoms] = useState([
    'Fever', 'Cough', 'Headache', 'Fatigue', 'Nausea', 'Vomiting',
    'Diarrhea', 'Abdominal Pain', 'Chest Pain', 'Shortness of Breath',
    'Dizziness', 'Muscle Pain', 'Joint Pain', 'Sore Throat', 'Runny Nose'
  ]);
  const [filteredSymptoms, setFilteredSymptoms] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  useEffect(() => {
    if (symptomInput) {
      const filtered = availableSymptoms.filter(symptom =>
        symptom.toLowerCase().includes(symptomInput.toLowerCase()) &&
        !symptoms.includes(symptom)
      );
      setFilteredSymptoms(filtered);
      setShowSuggestions(true);
    } else {
      setShowSuggestions(false);
    }
  }, [symptomInput, symptoms]);

  const addSymptom = (symptom) => {
    if (!symptoms.includes(symptom)) {
      setSymptoms([...symptoms, symptom]);
      setSymptomInput('');
      setShowSuggestions(false);
    }
  };

  const removeSymptom = (symptomToRemove) => {
    setSymptoms(symptoms.filter(symptom => symptom !== symptomToRemove));
  };

  const handleSymptomInputKeyPress = (e) => {
    if (e.key === 'Enter' && symptomInput.trim()) {
      addSymptom(symptomInput.trim());
    }
  };

  const analyzeSymptomsDemo = async () => {
    if (symptoms.length === 0) return;

    setLoading(true);
    
    // Simulate API call with demo data
    setTimeout(() => {
      const mockPredictions = [
        {
          disease: 'Common Cold',
          confidence: 85,
          description: 'A viral infection of the upper respiratory tract',
          recommendations: [
            'Get plenty of rest',
            'Stay hydrated',
            'Use over-the-counter pain relievers if needed',
            'Consider seeing a doctor if symptoms worsen'
          ]
        },
        {
          disease: 'Seasonal Flu',
          confidence: 72,
          description: 'A viral infection that affects the respiratory system',
          recommendations: [
            'Rest and stay home',
            'Drink plenty of fluids',
            'Consider antiviral medication',
            'Monitor for complications'
          ]
        },
        {
          disease: 'Migraine',
          confidence: 45,
          description: 'A type of headache characterized by severe pain',
          recommendations: [
            'Rest in a dark, quiet room',
            'Apply cold or warm compress',
            'Stay hydrated',
            'Consider prescription medication'
          ]
        }
      ];

      setPrediction({
        predictions: mockPredictions,
        timestamp: new Date().toISOString(),
        symptoms: [...symptoms]
      });
      setLoading(false);
    }, 2000);
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 80) return 'text-green-600 bg-green-100';
    if (confidence >= 60) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getConfidenceIcon = (confidence) => {
    if (confidence >= 80) return <CheckCircle className="w-5 h-5" />;
    if (confidence >= 60) return <AlertCircle className="w-5 h-5" />;
    return <AlertCircle className="w-5 h-5" />;
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center">
              <Brain className="w-8 h-8 text-white" />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            AI-Powered Diagnosis
          </h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Describe your symptoms and let our advanced AI analyze them to provide 
            potential diagnoses and recommendations. This is not a substitute for professional medical advice.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Symptom Input Section */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Enter Your Symptoms
              </h2>
              
              {/* Symptom Input */}
              <div className="relative mb-4">
                <Label htmlFor="symptom-input" className="text-sm font-medium text-gray-700 mb-2 block">
                  Add Symptom
                </Label>
                <div className="relative">
                  <Input
                    id="symptom-input"
                    type="text"
                    value={symptomInput}
                    onChange={(e) => setSymptomInput(e.target.value)}
                    onKeyPress={handleSymptomInputKeyPress}
                    placeholder="Type a symptom (e.g., fever, headache)"
                    className="pl-10"
                  />
                  <Search className="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                </div>
                
                {/* Symptom Suggestions */}
                {showSuggestions && filteredSymptoms.length > 0 && (
                  <div className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-md shadow-lg max-h-48 overflow-y-auto">
                    {filteredSymptoms.map((symptom, index) => (
                      <button
                        key={index}
                        onClick={() => addSymptom(symptom)}
                        className="w-full text-left px-4 py-2 hover:bg-gray-50 focus:bg-gray-50 focus:outline-none"
                      >
                        {symptom}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Selected Symptoms */}
              <div className="mb-6">
                <Label className="text-sm font-medium text-gray-700 mb-2 block">
                  Selected Symptoms ({symptoms.length})
                </Label>
                {symptoms.length === 0 ? (
                  <div className="text-gray-500 text-sm bg-gray-50 rounded-lg p-4 text-center">
                    No symptoms added yet. Start typing to add symptoms.
                  </div>
                ) : (
                  <div className="flex flex-wrap gap-2">
                    {symptoms.map((symptom, index) => (
                      <div
                        key={index}
                        className="flex items-center space-x-2 bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
                      >
                        <span>{symptom}</span>
                        <button
                          onClick={() => removeSymptom(symptom)}
                          className="hover:bg-blue-200 rounded-full p-1"
                        >
                          <X className="w-3 h-3" />
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Analyze Button */}
              <Button
                onClick={analyzeSymptomsDemo}
                disabled={symptoms.length === 0 || loading}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              >
                {loading ? (
                  <div className="flex items-center">
                    <Loader2 className="w-5 h-5 animate-spin mr-2" />
                    Analyzing Symptoms...
                  </div>
                ) : (
                  <div className="flex items-center">
                    <Brain className="w-5 h-5 mr-2" />
                    Analyze Symptoms
                  </div>
                )}
              </Button>

              {/* Disclaimer */}
              <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="flex items-start space-x-2">
                  <AlertCircle className="w-5 h-5 text-yellow-600 mt-0.5" />
                  <div className="text-sm text-yellow-800">
                    <strong>Medical Disclaimer:</strong> This AI diagnosis tool is for informational 
                    purposes only and should not replace professional medical advice. Always consult 
                    with a qualified healthcare provider for proper diagnosis and treatment.
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Activity className="w-5 h-5 text-blue-500" />
                    <span className="text-sm text-gray-600">Accuracy Rate</span>
                  </div>
                  <span className="text-sm font-semibold text-gray-900">95%</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Brain className="w-5 h-5 text-purple-500" />
                    <span className="text-sm text-gray-600">Diseases Covered</span>
                  </div>
                  <span className="text-sm font-semibold text-gray-900">500+</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <TrendingUp className="w-5 h-5 text-green-500" />
                    <span className="text-sm text-gray-600">Diagnoses Today</span>
                  </div>
                  <span className="text-sm font-semibold text-gray-900">1,247</span>
                </div>
              </div>
            </div>

            {/* Common Symptoms */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Common Symptoms</h3>
              <div className="space-y-2">
                {availableSymptoms.slice(0, 8).map((symptom, index) => (
                  <button
                    key={index}
                    onClick={() => addSymptom(symptom)}
                    disabled={symptoms.includes(symptom)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                      symptoms.includes(symptom)
                        ? 'bg-blue-100 text-blue-800 cursor-not-allowed'
                        : 'bg-gray-50 hover:bg-gray-100 text-gray-700'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span>{symptom}</span>
                      {symptoms.includes(symptom) ? (
                        <CheckCircle className="w-4 h-4" />
                      ) : (
                        <Plus className="w-4 h-4" />
                      )}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Prediction Results */}
        {prediction && (
          <div className="mt-8">
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">
                  Diagnosis Results
                </h2>
                <div className="text-sm text-gray-500">
                  Analyzed on {new Date(prediction.timestamp).toLocaleDateString()}
                </div>
              </div>

              <div className="space-y-6">
                {prediction.predictions.map((pred, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {pred.disease}
                      </h3>
                      <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm font-medium ${getConfidenceColor(pred.confidence)}`}>
                        {getConfidenceIcon(pred.confidence)}
                        <span>{pred.confidence}% confidence</span>
                      </div>
                    </div>
                    
                    <p className="text-gray-600 mb-4">{pred.description}</p>
                    
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-2">Recommendations:</h4>
                      <ul className="space-y-1">
                        {pred.recommendations.map((rec, recIndex) => (
                          <li key={recIndex} className="flex items-start space-x-2 text-sm text-gray-600">
                            <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                            <span>{rec}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>

              {/* Next Steps */}
              <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h4 className="font-semibold text-blue-900 mb-2">Next Steps</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Button variant="outline" className="flex items-center space-x-2">
                    <Calendar className="w-4 h-4" />
                    <span>Book Appointment</span>
                  </Button>
                  <Button variant="outline" className="flex items-center space-x-2">
                    <FileText className="w-4 h-4" />
                    <span>Save Report</span>
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Diagnosis;

