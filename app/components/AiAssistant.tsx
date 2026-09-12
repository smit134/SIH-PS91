"use client";

import { useState, useRef, useEffect } from "react";
import { Bot, X, Send, User, ChevronUp, ChevronDown } from "lucide-react";
import clsx from "clsx";

export default function AiAssistant() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hi! I'm ThinkForge Copilot. How can I help you today?" }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      // Gather context about the current page and user data
      let pageContent = "";
      try {
         // Extract text from the page to give the AI context of what the user sees
         pageContent = document.body.innerText.substring(0, 15000); 
      } catch (e) {
         console.warn("Failed to extract page content for AI context");
      }

      let userProfile = "";
      try {
         userProfile = localStorage.getItem("thinkforge_profile") || "No profile setup yet.";
      } catch (e) {
         console.warn("Failed to extract user profile for AI context");
      }

      const contextData = {
        pathname: window.location.pathname,
        title: document.title,
        page_text_content: pageContent,
        user_profile_data: userProfile
      };

      const res = await fetch("http://localhost:8000/api/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [...messages, { role: "user", content: userMessage }].map(m => ({
            role: m.role === "assistant" ? "model" : "user",
            content: m.content
          })),
          context_data: contextData
        })
      });

      if (res.ok) {
        const data = await res.json();
        setMessages(prev => [...prev, { role: "assistant", content: data.response }]);
      } else {
        setMessages(prev => [...prev, { role: "assistant", content: "Sorry, I'm having trouble connecting to the server right now." }]);
      }
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: "assistant", content: "Network error occurred." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
      {/* Chat Window */}
      {isOpen && (
        <div className="mb-4 w-80 sm:w-96 bg-white rounded-2xl shadow-2xl overflow-hidden border border-slate-200 flex flex-col transition-all duration-300 transform origin-bottom-right h-[500px] max-h-[80vh]">
          {/* Header */}
          <div className="bg-brand-600 text-white p-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Bot className="w-5 h-5" />
              <h3 className="font-semibold text-sm">ThinkForge Copilot</h3>
            </div>
            <button onClick={() => setIsOpen(false)} className="text-brand-100 hover:text-white transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 p-4 overflow-y-auto bg-slate-50 flex flex-col gap-3">
            {messages.map((msg, idx) => (
              <div key={idx} className={clsx(
                "flex items-start gap-2 max-w-[85%]",
                msg.role === "user" ? "self-end flex-row-reverse" : "self-start"
              )}>
                <div className={clsx(
                  "w-6 h-6 rounded-full flex items-center justify-center shrink-0",
                  msg.role === "user" ? "bg-slate-200" : "bg-brand-100 text-brand-600"
                )}>
                  {msg.role === "user" ? <User className="w-3 h-3 text-slate-600" /> : <Bot className="w-3 h-3" />}
                </div>
                <div className={clsx(
                  "p-3 rounded-xl text-sm shadow-sm whitespace-pre-wrap",
                  msg.role === "user" ? "bg-brand-600 text-white rounded-tr-sm" : "bg-white text-slate-700 rounded-tl-sm border border-slate-100"
                )}>
                  {msg.content}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex items-start gap-2 max-w-[85%] self-start">
                <div className="w-6 h-6 rounded-full bg-brand-100 text-brand-600 flex items-center justify-center shrink-0">
                  <Bot className="w-3 h-3" />
                </div>
                <div className="p-3 bg-white text-slate-700 rounded-xl rounded-tl-sm border border-slate-100 shadow-sm flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 bg-brand-400 rounded-full animate-bounce" />
                  <div className="w-1.5 h-1.5 bg-brand-400 rounded-full animate-bounce [animation-delay:0.2s]" />
                  <div className="w-1.5 h-1.5 bg-brand-400 rounded-full animate-bounce [animation-delay:0.4s]" />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-3 bg-white border-t border-slate-100">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
              className="flex items-center gap-2 relative"
            >
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask me anything..."
                className="w-full bg-slate-50 border border-slate-200 rounded-full py-2.5 pl-4 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
              />
              <button
                type="submit"
                disabled={!input.trim() || isLoading}
                className="absolute right-1.5 p-1.5 bg-brand-600 text-white rounded-full hover:bg-brand-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={clsx(
          "w-14 h-14 rounded-full flex items-center justify-center shadow-lg transition-transform hover:scale-105 active:scale-95",
          isOpen ? "bg-slate-800 text-white" : "bg-brand-600 text-white"
        )}
      >
        {isOpen ? <ChevronDown className="w-6 h-6" /> : <Bot className="w-6 h-6" />}
      </button>
    </div>
  );
}
