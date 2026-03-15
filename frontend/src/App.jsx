import { useState, useRef, useEffect } from "react";
import { Send, Menu, Upload, FileText, Loader2, Bot, User } from "lucide-react";

function App() {
  const [messages, setMessages] = useState([
    { id: 1, role: "assistant", content: "Hi! I am DocuMind. Upload a document to get started." }
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const [documents, setDocuments] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const newMsg = { id: Date.now(), role: "user", content: inputMessage };
    setMessages((prev) => [...prev, newMsg]);
    setInputMessage("");
    setIsTyping(true);

    // Simulate API delay for asking a question
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          role: "assistant",
          content: "This is a placeholder response from DocuMind. We haven't connected the backend API yet."
        }
      ]);
      setIsTyping(false);
    }, 1500);
  };

  const handleFileUpload = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    
    // Simulate upload delay
    setTimeout(() => {
      setDocuments((prev) => [...prev, { name: file.name, size: (file.size / 1024 / 1024).toFixed(2) }]);
      setIsUploading(false);
      setMessages((prev) => [
        ...prev, 
        { id: Date.now(), role: "assistant", content: `I've successfully processed "${file.name}". What would you like to know about it?` }
      ]);
    }, 2000);
  };

  return (
    <div className="flex h-screen bg-neutral-900 text-neutral-100 font-sans">
      
      {/* Sidebar for Documents */}
      <div 
        className={`${isSidebarOpen ? 'w-72' : 'w-0'} transition-all duration-300 ease-in-out bg-neutral-950 border-r border-neutral-800 flex flex-col overflow-hidden`}
      >
        <div className="p-4 flex flex-col h-full w-72">
          <h2 className="text-xl font-bold tracking-tight text-white mb-6">DocuMind</h2>
          
          <button 
            onClick={() => fileInputRef.current?.click()}
            disabled={isUploading}
            className="flex items-center justify-center gap-2 w-full py-3 px-4 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white rounded-lg font-medium transition-colors mb-6"
          >
            {isUploading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Upload className="w-5 h-5" />}
            {isUploading ? "Uploading..." : "Upload PDF"}
          </button>
          
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileUpload} 
            accept=".pdf" 
            className="hidden" 
          />

          <div className="flex-1 overflow-y-auto">
            <h3 className="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-3">Your Documents</h3>
            {documents.length === 0 ? (
              <p className="text-sm text-neutral-500 text-center mt-10">No documents uploaded yet.</p>
            ) : (
              <div className="space-y-2">
                {documents.map((doc, i) => (
                  <div key={i} className="flex items-center gap-3 p-3 bg-neutral-900 rounded-lg border border-neutral-800 group hover:border-neutral-700 cursor-pointer">
                    <FileText className="w-5 h-5 text-indigo-400" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-neutral-200 truncate">{doc.name}</p>
                      <p className="text-xs text-neutral-500">{doc.size} MB</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0 bg-neutral-900">
        
        {/* Header */}
        <header className="h-16 flex items-center px-4 border-b border-neutral-800 shrink-0">
          <button 
            onClick={() => setSidebarOpen(!isSidebarOpen)}
            className="p-2 hover:bg-neutral-800 rounded-lg transition-colors text-neutral-400"
          >
            <Menu className="w-6 h-6" />
          </button>
          <span className="ml-4 font-medium text-neutral-200">
            {documents.length > 0 ? `Chatting with ${documents.length} document(s)` : "New Chat"}
          </span>
        </header>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
          {messages.map((msg) => (
            <div 
              key={msg.id} 
              className={`flex gap-4 max-w-4xl mx-auto ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
            >
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-indigo-600' : 'bg-emerald-600'}`}>
                {msg.role === 'user' ? <User className="w-5 h-5 text-white" /> : <Bot className="w-5 h-5 text-white" />}
              </div>
              <div className={`flex flex-col max-w-[80%] ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                <div 
                  className={`px-5 py-3.5 rounded-2xl text-[15px] leading-relaxed ${
                    msg.role === 'user' 
                      ? 'bg-neutral-800 text-neutral-100 rounded-tr-none' 
                      : 'text-neutral-200'
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex gap-4 max-w-4xl mx-auto">
              <div className="w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center shrink-0">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="flex items-center text-neutral-400 px-5 py-3.5">
                <Loader2 className="w-5 h-5 animate-spin" />
                <span className="ml-3 text-sm">Thinking...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-neutral-900 border-t border-neutral-800">
          <div className="max-w-4xl mx-auto">
            <form 
              onSubmit={handleSendMessage}
              className="relative flex items-end gap-2 bg-neutral-800 rounded-xl border border-neutral-700 focus-within:border-neutral-500 focus-within:ring-1 focus-within:ring-neutral-500 transition-all p-2"
            >
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSendMessage(e);
                  }
                }}
                placeholder={documents.length > 0 ? "Ask a question about your documents..." : "Upload a document to start asking questions..."}
                className="w-full bg-transparent text-neutral-100 placeholder-neutral-500 border-0 focus:ring-0 resize-none py-3 px-3 min-h-[52px] max-h-48"
                rows={1}
                disabled={isTyping}
              />
              <button
                type="submit"
                disabled={!inputMessage.trim() || isTyping}
                className="p-3 bg-indigo-600 hover:bg-indigo-700 disabled:bg-neutral-700 disabled:text-neutral-500 text-white rounded-lg transition-colors flex-shrink-0"
              >
                <Send className="w-5 h-5" />
              </button>
            </form>
            <p className="text-center text-xs text-neutral-600 mt-3">
              DocuMind can make mistakes. Check important info from the documents.
            </p>
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;
