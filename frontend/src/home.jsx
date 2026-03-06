import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import AMLGraph from "./AMLGraph.jsx";

const BASE_URL = "http://127.0.0.1:8000/api";

export default function GraphGuardHome() {

  const navigate = useNavigate();

  const csvInputRef = useRef(null);

  const [canAnalyze, setCanAnalyze] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [popupMessage, setPopupMessage] = useState("");
  const [popupType, setPopupType] = useState("success");
  const [showGraph, setShowGraph] = useState(false);
  const [showUploader, setShowUploader] = useState(false);

  useEffect(() => {

    const csvInput = csvInputRef.current;

    if (!csvInput) return;

    const onFileChange = () => {

      const file = csvInput.files[0];

      setCanAnalyze(false);

      if (!file || !file.name.endsWith(".csv")) {
        showError("Please upload a valid CSV file.");
        return;
      }

      const reader = new FileReader();

      reader.onload = e => {

        const text = e.target.result;

        const lines = text.split("\n");

        if (lines.length < 2 || !lines[0].includes(",")) {
          showError("Invalid CSV structure.");
          return;
        }

        showSuccess("Valid CSV detected. Ready to upload.");

      };

      reader.readAsText(file);

    };

    csvInput.addEventListener("change", onFileChange);

    return () => csvInput.removeEventListener("change", onFileChange);

  }, []);

  const showSuccess = msg => {
    setPopupType("success");
    setPopupMessage(msg);
    setShowPopup(true);
  };

  const showError = msg => {
    setPopupType("error");
    setPopupMessage(msg);
    setShowPopup(true);
  };

  const uploadCsv = async () => {

    const file = csvInputRef.current.files[0];

    if (!file) return;

    const formData = new FormData();

    formData.append("file", file);

    try {

      const res = await fetch(`${BASE_URL}/upload-csv/`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error();

      setCanAnalyze(true);

      showSuccess("CSV uploaded successfully.");

    } catch {

      showError("CSV upload failed.");

    }

  };

  const analyze = async () => {

    try {

      const res = await fetch(`${BASE_URL}/analyze/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });

      if (!res.ok) throw new Error();

      showSuccess("Analysis started. Rendering graph…");

      setShowGraph(true);

    } catch {

      showError("Analysis failed.");

    }

  };

  return (
  <div className="min-h-screen bg-gradient-to-b from-white via-blue-50 to-gray-100 text-gray-800 relative overflow-hidden">

    {/* Background Glow */}
    <div className="absolute top-[-200px] left-1/2 -translate-x-1/2 w-[800px] h-[800px] bg-blue-200 opacity-20 blur-[180px] rounded-full"></div>

    {showPopup && (
      <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">

        <div className="bg-white border border-gray-200 rounded-2xl p-6 w-[360px] shadow-xl text-center">

          <h3 className="text-base font-semibold text-gray-900 mb-2">
            {popupType === "success" ? "Status" : "Error"}
          </h3>

          <p className="text-gray-500 mb-6 text-sm">
            {popupMessage}
          </p>

          <button
            onClick={() => setShowPopup(false)}
            className="px-6 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition"
          >
            Close
          </button>

        </div>

      </div>
    )}

    {!showGraph && (

      <main className="relative min-h-screen flex items-center justify-center px-6">

        <div className="max-w-4xl w-full text-center animate-fadein">

          {/* Title */}
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 leading-tight">
            Yeh Kala Dhan
            <span className="text-blue-600 block">
              Mujhe De De Thakur!
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-gray-500 mt-6 text-lg max-w-2xl mx-auto">
            The “Smurfing” Hunter — Detecting Money Laundering Circles in
            Blockchain and Banking Transaction Graphs using Hybrid Graph Intelligence.
          </p>

          {!showUploader && (
            <>
              {/* Buttons */}
              <div className="mt-12 flex justify-center gap-6 flex-wrap">

                <button
                  onClick={() => setShowUploader(true)}
                  className="px-10 py-4 rounded-xl bg-blue-600 text-white font-semibold shadow-md hover:bg-blue-700 hover:scale-105 transition-all"
                >
                  Explore Live Graph
                </button>

                <button
                  onClick={() => navigate("/how-it-works")}
                  className="px-10 py-4 rounded-xl font-semibold border border-gray-300 hover:bg-gray-100 transition-all"
                >
                  How it Works
                </button>

              </div>

              {/* Stats Cards */}
              <div className="mt-14 grid grid-cols-1 md:grid-cols-3 gap-6">

                <div className="bg-white border border-gray-200 shadow-sm rounded-xl p-6 text-sm text-gray-600 hover:shadow-lg transition hover:-translate-y-1">
                  <div className="text-2xl font-bold text-blue-600 mb-2">
                    $2T+
                  </div>
                  Laundered annually — nearly 5-10% of global GDP.
                </div>

                <div className="bg-white border border-gray-200 shadow-sm rounded-xl p-6 text-sm text-gray-600 hover:shadow-lg transition hover:-translate-y-1">
                  <div className="text-2xl font-bold text-blue-600 mb-2">
                    90%
                  </div>
                  Of crypto mixing goes undetected due to complex transaction webs.
                </div>

                <div className="bg-white border border-gray-200 shadow-sm rounded-xl p-6 text-sm text-gray-600 hover:shadow-lg transition hover:-translate-y-1">
                  <div className="text-2xl font-bold text-blue-600 mb-2">
                    Smurfing
                  </div>
                  Networks evade detection by staying under threshold limits.
                </div>

              </div>
            </>
          )}

          {showUploader && (
            <div className="mt-12 max-w-xl mx-auto bg-white border border-gray-200 shadow-lg rounded-2xl p-8 animate-slideup">

              <input
                ref={csvInputRef}
                type="file"
                accept=".csv"
                className="w-full text-sm text-gray-600 border border-gray-300 rounded-lg px-3 py-3 bg-white hover:border-blue-400 transition"
              />

              <button
                onClick={uploadCsv}
                className="mt-6 w-full px-6 py-3 rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition"
              >
                Upload Transactions
              </button>

              <button
                disabled={!canAnalyze}
                onClick={analyze}
                className={`mt-4 w-full px-6 py-3 rounded-xl transition ${
                  canAnalyze
                    ? "bg-blue-600 text-white hover:bg-blue-700"
                    : "bg-gray-200 text-gray-400 cursor-not-allowed"
                }`}
              >
                Analyze Transactions
              </button>

            </div>
          )}

        </div>

      </main>
    )}

    {showGraph && <AMLGraph />}

  </div>
);
}