"use client";

import { useState, useEffect } from "react";
import { Loader2, ExternalLink, Copy, Check, FileText } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [url, setUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<{
    transcription: string;
    reel_id: string;
    processing_time: number;
  } | null>(null);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);
  const [isBackendOnline, setIsBackendOnline] = useState<boolean | null>(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch(`${API_URL}/health`, { method: "GET" });
        setIsBackendOnline(response.ok);
      } catch {
        setIsBackendOnline(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url) return;

    setIsLoading(true);
    setError("");
    setResult(null);

    // Basic URL validation
    if (!url.includes("instagram.com/reel/")) {
      setError("Please enter a valid Instagram Reel URL");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_URL}/api/transcribe`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reel_url: url }),
      });

      const data = await response.json();

      if (data.status === "success") {
        setResult({
          transcription: data.transcription,
          reel_id: data.reel_id,
          processing_time: data.processing_time,
        });
      } else {
        setError(data.message || "Something went wrong failed to transcribe.");
      }
    } catch (err) {
      setError("Failed to connect to the backend server. Is it running?");
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = () => {
    if (result?.transcription) {
      navigator.clipboard.writeText(result.transcription);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <main className="min-h-screen bg-black text-white font-sans selection:bg-purple-500/30">
      {/* Background Gradients */}
      <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-purple-900/20 blur-[100px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-blue-900/20 blur-[100px]" />
      </div>

      <div className="relative z-10 max-w-3xl mx-auto px-4 py-20 flex flex-col items-center">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className={`inline-flex items-center gap-2 mb-4 px-3 py-1 rounded-full border text-xs font-medium ${isBackendOnline === null
              ? "bg-white/5 border-white/10 text-gray-400"
              : isBackendOnline
                ? "bg-green-500/10 border-green-500/20 text-green-300"
                : "bg-red-500/10 border-red-500/20 text-red-300"
            }`}>
            <span className="relative flex h-2 w-2">
              {isBackendOnline !== false && (
                <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${isBackendOnline === null ? "bg-gray-400" : "bg-green-400"
                  }`}></span>
              )}
              <span className={`relative inline-flex rounded-full h-2 w-2 ${isBackendOnline === null
                  ? "bg-gray-500"
                  : isBackendOnline
                    ? "bg-green-500"
                    : "bg-red-500"
                }`}></span>
            </span>
            {isBackendOnline === null
              ? "Connecting..."
              : isBackendOnline
                ? "Backend Connected"
                : "Backend Offline"}
          </div>
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-4 bg-gradient-to-br from-white via-white to-gray-500 bg-clip-text text-transparent">
            InstaTranscriber
          </h1>
          <p className="text-lg text-gray-400 max-w-lg mx-auto">
            Turn Instagram Reels into clear text in seconds using advanced AI.
          </p>
        </motion.div>

        {/* Input Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="w-full bg-white/5 border border-white/10 rounded-2xl p-2 shadow-2xl backdrop-blur-xl"
        >
          <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-2">
            <input
              type="text"
              placeholder="Paste Instagram Reel URL here..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="flex-1 bg-transparent border border-transparent focus:border-purple-500/50 rounded-xl px-4 py-4 text-white placeholder-gray-500 outline-none transition-all duration-300"
            />
            <button
              type="submit"
              disabled={isLoading || !url}
              className="group bg-white text-black font-semibold rounded-xl px-8 py-4 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 transition-all duration-300 flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <>
                  Transcribe <ExternalLink className="w-4 h-4 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
                </>
              )}
            </button>
          </form>
        </motion.div>

        {/* Error Message */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="w-full mt-4 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-200 text-center text-sm"
            >
              {error}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Result Section */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="w-full mt-8 space-y-4"
            >

              {/* Stats */}
              <div className="flex justify-between items-center px-2 text-sm text-gray-400">
                <span className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-green-500" /> Done in {result.processing_time.toFixed(2)}s
                </span>
                <span>ID: {result.reel_id}</span>
              </div>

              {/* Card */}
              <div className="bg-[#111] border border-white/10 rounded-2xl overflow-hidden shadow-2xl">
                {/* Toolbar */}
                <div className="flex items-center justify-between px-4 py-3 border-b border-white/5 bg-white/5">
                  <div className="flex items-center gap-2 text-gray-400">
                    <FileText className="w-4 h-4" />
                    <span className="text-xs font-medium uppercase tracking-wider">Transcription</span>
                  </div>
                  <button
                    onClick={copyToClipboard}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-xs font-medium text-gray-300 transition-colors"
                  >
                    {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
                    {copied ? "Copied" : "Copy Text"}
                  </button>
                </div>

                {/* Content */}
                <div className="p-6 max-h-[500px] overflow-y-auto custom-scrollbar">
                  <p className="text-gray-200 leading-relaxed whitespace-pre-wrap text-[15px]">
                    {result.transcription}
                  </p>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </main>
  );
}
