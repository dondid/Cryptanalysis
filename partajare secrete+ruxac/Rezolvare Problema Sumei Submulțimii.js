import React, { useState, useEffect } from 'react';

export default function SubsetSumSolver() {
  const [numbers, setNumbers] = useState('7, 3, 2, 5, 8');
  const [targetSum, setTargetSum] = useState('10');
  const [results, setResults] = useState(null);
  const [steps, setSteps] = useState([]);
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  
  // Funcția care rezolvă problema subset sum
  const solveSubsetSum = () => {
    setLoading(true);
    
    // Parsarea datelor de intrare
    const numArray = numbers.split(',').map(num => parseInt(num.trim())).filter(num => !isNaN(num));
    const target = parseInt(targetSum);
    
    if (numArray.length === 0 || isNaN(target)) {
      setResults({ possible: false, solution: null });
      setSteps([{ text: "Datele de intrare nu sunt valide.", solution: null }]);
      setLoading(false);
      return;
    }
    
    // Inițializarea pașilor de rezolvare
    const newSteps = [];
    
    newSteps.push({
      text: `Problema subset sum: Avem mulțimea {${numArray.join(', ')}} și căutăm o submulțime care să aibă suma ${target}.`,
      solution: null
    });
    
    newSteps.push({
      text: "În termeni matematici, căutăm valori xi ∈ {0,1} astfel încât ∑(xi·ai) = S.",
      solution: null
    });
    
    // Algoritm de backtracking pentru găsirea unei soluții
    const findSubset = (arr, target) => {
      // Folosim programare dinamică pentru eficiență
      const dp = new Array(arr.length + 1).fill().map(() => new Array(target + 1).fill(false));
      
      // Cazul de bază: putem forma suma 0 fără să folosim niciun element
      for (let i = 0; i <= arr.length; i++) {
        dp[i][0] = true;
      }
      
      // Completăm tabelul dp
      for (let i = 1; i <= arr.length; i++) {
        for (let j = 1; j <= target; j++) {
          if (j < arr[i-1]) {
            // Nu putem include elementul curent
            dp[i][j] = dp[i-1][j];
          } else {
            // Putem include sau exclude elementul curent
            dp[i][j] = dp[i-1][j] || dp[i-1][j - arr[i-1]];
          }
        }
      }
      
      // Verificăm dacă este posibilă formarea sumei target
      if (!dp[arr.length][target]) {
        return { possible: false, solution: null };
      }
      
      // Reconstruim soluția
      const solution = new Array(arr.length).fill(0);
      let remaining = target;
      
      for (let i = arr.length; i > 0 && remaining > 0; i--) {
        // Dacă putem forma suma remaining fără elementul curent, îl excludem
        if (dp[i-1][remaining]) {
          continue;
        } else {
          // Altfel, includem elementul curent
          solution[i-1] = 1;
          remaining -= arr[i-1];
        }
      }
      
      return { possible: true, solution };
    };
    
    // Adăugăm pași intermediari pentru explicarea algoritmului
    newSteps.push({
      text: "Pentru rezolvare, folosim programare dinamică (metoda tabelară).",
      solution: null
    });
    
    newSteps.push({
      text: "Construim un tabel dp[i][j] care indică dacă putem forma suma j folosind primele i elemente din mulțime.",
      solution: null
    });
    
    // Executăm algoritmul
    const result = findSubset(numArray, target);
    
    // Adăugăm rezultatul în pași
    if (result.possible) {
      const usedElements = numArray.filter((_, index) => result.solution[index] === 1);
      
      newSteps.push({
        text: `Am găsit o soluție! Putem forma suma ${target} folosind submulțimea {${usedElements.join(', ')}}.`,
        solution: result.solution
      });
      
      // Verificare matematică
      const sum = usedElements.reduce((acc, curr) => acc + curr, 0);
      newSteps.push({
        text: `Verificare: ${usedElements.join(' + ')} = ${sum}`,
        solution: result.solution
      });
      
      // Interpretare matematică
      const interpretation = numArray.map((num, idx) => 
        result.solution[idx] === 1 ? `1×${num}` : `0×${num}`
      ).join(' + ');
      
      newSteps.push({
        text: `În notația matematică din problemă: ${interpretation} = ${target}`,
        solution: result.solution
      });
    } else {
      newSteps.push({
        text: `Nu există o submulțime care să aibă suma ${target}.`,
        solution: null
      });
    }
    
    setSteps(newSteps);
    setResults(result);
    setCurrentStep(0);
    setLoading(false);
  };
  
  useEffect(() => {
    solveSubsetSum();
  }, []);
  
  // Funcții pentru navigarea prin pași
  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };
  
  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };
  
  return (
    <div className="max-w-4xl mx-auto p-4 bg-gray-50 rounded-lg shadow-md">
      <h1 className="text-2xl font-bold text-center mb-4">Rezolvare Problema Sumei Submulțimii</h1>
      
      <div className="mb-6 bg-yellow-50 p-4 rounded-md border border-yellow-200">
        <h2 className="text-lg font-medium mb-2">Problema:</h2>
        <div className="space-y-2">
          <p>Considerăm {`{a₁, a₂, ..., aₙ}`} o mulțime de numere naturale</p>
          <p>S un număr natural.</p>
          <p>Să se determine dacă există xᵢ ∈ {`{0,1}`}, 1 ≤ i ≤ n, pentru care:</p>
          <p className="text-center">∑(xᵢ·aᵢ) = S</p>
        </div>
      </div>
      
      <div className="mb-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block mb-1 font-medium">Mulțimea de numere (separate prin virgulă):</label>
          <input 
            type="text" 
            value={numbers} 
            onChange={(e) => setNumbers(e.target.value)} 
            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block mb-1 font-medium">Suma dorită (S):</label>
          <input 
            type="text" 
            value={targetSum} 
            onChange={(e) => setTargetSum(e.target.value)} 
            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
      
      <button 
        onClick={solveSubsetSum} 
        className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition mb-6"
        disabled={loading}
      >
        {loading ? 'Se calculează...' : 'Rezolvă'}
      </button>
      
      {steps.length > 0 && (
        <div className="bg-white p-4 rounded-md border mb-4">
          <h3 className="font-medium mb-2">Explicație pas cu pas:</h3>
          <div className="mb-4 min-h-32 py-3">
            <p>{steps[currentStep].text}</p>
            
            {steps[currentStep].solution && (
              <div className="mt-3 overflow-x-auto">
                <table className="table-auto border-collapse w-full mt-2">
                  <thead>
                    <tr>
                      <th className="border px-2 py-1">Elementele</th>
                      {numbers.split(',').map((num, idx) => (
                        <th key={idx} className="border px-2 py-1">{num.trim()}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td className="border px-2 py-1 font-medium">Valori xᵢ</td>
                      {steps[currentStep].solution.map((val, idx) => (
                        <td key={idx} className={`border px-2 py-1 text-center ${val === 1 ? 'bg-green-100' : ''}`}>
                          {val}
                        </td>
                      ))}
                    </tr>
                  </tbody>
                </table>
              </div>
            )}
          </div>
          
          <div className="flex justify-between">
            <button 
              onClick={prevStep} 
              disabled={currentStep === 0}
              className={`px-4 py-1 rounded ${currentStep === 0 ? 'bg-gray-300' : 'bg-blue-600 text-white hover:bg-blue-700'}`}
            >
              Înapoi
            </button>
            <span className="py-1">{currentStep + 1} / {steps.length}</span>
            <button 
              onClick={nextStep} 
              disabled={currentStep === steps.length - 1}
              className={`px-4 py-1 rounded ${currentStep === steps.length - 1 ? 'bg-gray-300' : 'bg-blue-600 text-white hover:bg-blue-700'}`}
            >
              Înainte
            </button>
          </div>
        </div>
      )}
      
      {results && (
        <div className={`p-4 rounded-md border ${results.possible ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
          <h3 className="font-medium mb-2">Rezultat final:</h3>
          {results.possible ? (
            <p>
              DA, există o submulțime care are suma {targetSum}.
            </p>
          ) : (
            <p>
              NU există o submulțime care are suma {targetSum}.
            </p>
          )}
        </div>
      )}
    </div>
  );
}