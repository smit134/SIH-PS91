"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Lock, Phone, ArrowRight, Sparkles } from "lucide-react";

export default function AuthPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const res = await fetch("http://localhost:8000/users/auth", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone })
      });

      if (res.ok) {
        const data = await res.json();
        localStorage.setItem("thinkforge_token", data.user_id);
        localStorage.setItem("thinkforge_phone", phone);
        
        if (data.name) {
          localStorage.setItem("thinkforge_name", data.name);
        } else if (!isLogin && name) {
          localStorage.setItem("thinkforge_name", name);
        }

        if (data.has_profile) {
          router.push("/dashboard");
        } else {
          router.push("/register");
        }
      } else {
        console.error("Auth failed");
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full flex-1 flex items-center justify-center py-10 px-4">
      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-brand-500/10 text-brand-400 border border-brand-500/20 mb-4">
            <Sparkles className="w-6 h-6" />
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">
            {isLogin ? "Welcome back to ThinkForge" : "Create your account"}
          </h1>
          <p className="text-sm text-slate-400 mt-2">
            {isLogin 
              ? "Sign in to access your dashboard and opportunities." 
              : "Sign up to start your entrepreneurial journey."}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">Full Name</label>
              <div className="relative">
                <div className="absolute left-3.5 top-3 w-4 h-4 text-slate-500 flex items-center justify-center font-bold">@</div>
                <input 
                  type="text" 
                  required={!isLogin}
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Ramesh Kumar"
                  className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 transition-all"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">Phone Number</label>
            <div className="relative">
              <Phone className="absolute left-3.5 top-3 w-4 h-4 text-slate-500" />
              <input 
                type="tel" 
                required
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="+91 98765 43210"
                className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 transition-all"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">Password</label>
            <div className="relative">
              <Lock className="absolute left-3.5 top-3 w-4 h-4 text-slate-500" />
              <input 
                type="password" 
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 transition-all"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-2 inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl text-sm font-bold bg-gradient-to-r from-brand-600 to-teal-600 text-white hover:opacity-95 shadow-glow-teal transition-all disabled:opacity-50"
          >
            {loading ? "Authenticating..." : (isLogin ? "Sign In" : "Sign Up")}
            {!loading && <ArrowRight className="w-4 h-4" />}
          </button>
        </form>

        <div className="mt-6 text-center text-xs text-slate-400">
          {isLogin ? "Don't have an account?" : "Already have an account?"}
          <button 
            type="button"
            onClick={() => setIsLogin(!isLogin)}
            className="ml-1.5 text-brand-400 hover:text-brand-300 font-semibold transition-colors"
          >
            {isLogin ? "Sign up" : "Sign in"}
          </button>
        </div>
      </div>
    </div>
  );
}
