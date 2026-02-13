# ++==Front end - App Router (sec/App.tsx)==++  
  
import { Switch, Route } from "wouter";  
import { queryClient } from "./lib/queryClient";  
import { QueryClientProvider } from "@tanstack/react-query";  
import { Toaster } from "@/components/ui/toaster";  
import { TooltipProvider } from "@/components/ui/tooltip";  
import NotFound from "@/pages/not-found";  
import ProtocolPage from "@/pages/protocol";  
import AuthPage from "@/pages/auth";  
import DashboardGSP from "@/pages/dashboard-gsp";  
  
function Router() {  
  return (  
    <Switch>  
      <Route path="/" component={ProtocolPage} />  
      <Route path="/auth" component={AuthPage} />  
      <Route path="/dashboard" component={DashboardGSP} />  
      <Route component={NotFound} />  
    </Switch>  
  );  
}  
  
export default function App() {  
  return (  
    <QueryClientProvider client={queryClient}>  
      <TooltipProvider>  
        <Toaster />  
        <Router />  
      </TooltipProvider>  
    </QueryClientProvider>  
  );  
}  
  
# ++==Front end-Protocol page (src/pages/protocol.tsx)==++  
  
import { useState } from "react";  
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";  
import { Button } from "@/components/ui/button";  
import { Badge } from "@/components/ui/badge";  
import { CheckCircle, Shield, Lock, Zap, GitBranch, Eye } from "lucide-react";  
  
interface Attestation {  
  id: string;  
  action: string;  
  timestamp: string;  
  userId: string;  
  hash: string;  
  verified: boolean;  
}  
  
export default function ProtocolPage() {  
  const [attestations, setAttestations] = useState<Attestation[]>([  
    {  
      id: "att-001",  
      action: "INIT",  
      timestamp: "2025-12-31T03:54:12Z",  
      userId: "usr-alpha-001",  
      hash: "0x7a3f8c2e1b9d4a6e5f3c2b1a",  
      verified: true  
    },  
    {  
      id: "att-002",  
      action: "AUDIT",  
      timestamp: "2025-12-31T03:52:45Z",  
      userId: "usr-beta-002",  
      hash: "0x4e2d9c3a1f7b5e8c2d6a3f1e",  
      verified: true  
    },  
    {  
      id: "att-003",  
      action: "POLICY_BIND",  
      timestamp: "2025-12-31T03:50:18Z",  
      userId: "usr-gamma-003",  
      hash: "0x9b1c4d7e2a5f8c3b6e1d4a2f",  
      verified: true  
    }  
  ]);  
  
  const [logs, setLogs] = useState<string[]>([  
    "[03:54:12] Protocol initialized",  
    "[03:52:45] Attestation logged",  
    "[03:50:18] Policy binding verified",  
    "[03:48:30] Chain synchronized"  
  ]);  
  
  const handleLogAction = () => {  
    const action = `[${new Date().toLocaleTimeString("en-US", { hour12: false })}] Action logged`;  
    setLogs([action, ...logs]);  
  };  
  
  return (  
    <div className="min-h-screen bg-background text-foreground">  
      <div className="border-b border-border/30 bg-gradient-to-b from-card/50 to-background">  
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">  
          <div className="space-y-6">  
            <div className="flex items-center gap-3">  
              <div className="h-12 w-12 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center">  
                <Shield className="h-7 w-7 text-primary-foreground" />  
              </div>  
              <div>  
                <h1 className="text-4xl sm:text-5xl font-bold tracking-tight">Glass Substrate Protocol</h1>  
                <p className="text-primary mt-1 font-mono text-sm">Universal AI Accountability Framework</p>  
              </div>  
            </div>  
              
            <div className="space-y-3">  
              <p className="text-lg text-muted-foreground max-w-3xl leading-relaxed">  
                A cryptographic governance layer that makes AI systems accountable, transparent, and verifiable across any deployment. GSP holds AI responsible through immutable attestation, policy binding, and portable audit trails.  
              </p>  
                
              <div className="flex flex-wrap gap-2">  
                <Badge className="bg-primary/20 text-primary border-primary/30">Accountability</Badge>  
                <Badge className="bg-secondary/20 text-secondary border-secondary/30">Governance</Badge>  
                <Badge className="bg-accent/20 text-accent border-accent/30">Transparency</Badge>  
              </div>  
            </div>  
          </div>  
        </div>  
      </div>  
  
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-8">  
        <div>  
          <h2 className="text-2xl font-bold tracking-tight mb-6">Core Principles</h2>  
          <div className="grid gap-4 md:grid-cols-3">  
            <Card className="border-border/50">  
              <CardHeader>  
                <CardTitle className="text-base flex items-center gap-2">  
                  <Eye className="h-5 w-5 text-primary" />  
                  Transparency  
                </CardTitle>  
              </CardHeader>  
              <CardContent className="text-sm text-muted-foreground">  
                Every AI decision is logged, auditable, and cryptographically bound to its policy.  
              </CardContent>  
            </Card>  
  
            <Card className="border-border/50">  
              <CardHeader>  
                <CardTitle className="text-base flex items-center gap-2">  
                  <Lock className="h-5 w-5 text-secondary" />  
                  Accountability  
                </CardTitle>  
              </CardHeader>  
              <CardContent className="text-sm text-muted-foreground">  
                Immutable attestations prove which model, policy, and user made each decision.  
              </CardContent>  
            </Card>  
  
            <Card className="border-border/50">  
              <CardHeader>  
                <CardTitle className="text-base flex items-center gap-2">  
                  <GitBranch className="h-5 w-5 text-accent" />  
                  Portable  
                </CardTitle>  
              </CardHeader>  
              <CardContent className="text-sm text-muted-foreground">  
                Governance receipts move with your AI across systems, environments, and jurisdictions.  
              </CardContent>  
            </Card>  
          </div>  
        </div>  
  
        <div className="space-y-6">  
          <h2 className="text-2xl font-bold tracking-tight">Protocol Status</h2>  
            
          <div className="grid gap-4 md:grid-cols-3">  
            <Card className="border-border/50">  
              <CardHeader className="pb-3">  
                <CardTitle className="text-sm font-medium flex items-center gap-2">  
                  <CheckCircle className="h-4 w-4 text-primary" />  
                  Status  
                </CardTitle>  
              </CardHeader>  
              <CardContent>  
                <div className="text-2xl font-bold">Active</div>  
                <p className="text-xs text-muted-foreground mt-1">All systems operational</p>  
              </CardContent>  
            </Card>  
  
            <Card className="border-border/50">  
              <CardHeader className="pb-3">  
                <CardTitle className="text-sm font-medium flex items-center gap-2">  
                  <Lock className="h-4 w-4 text-secondary" />  
                  Attestations  
                </CardTitle>  
              </CardHeader>  
              <CardContent>  
                <div className="text-2xl font-bold">{attestations.length}</div>  
                <p className="text-xs text-muted-foreground mt-1">Verified & immutable</p>  
              </CardContent>  
            </Card>  
  
            <Card className="border-border/50">  
              <CardHeader className="pb-3">  
                <CardTitle className="text-sm font-medium flex items-center gap-2">  
                  <Zap className="h-4 w-4 text-accent" />  
                  Coverage  
                </CardTitle>  
              </CardHeader>  
              <CardContent>  
                <div className="text-2xl font-bold">Universal</div>  
                <p className="text-xs text-muted-foreground mt-1">Any AI system, any deployment</p>  
              </CardContent>  
            </Card>  
          </div>  
        </div>  
  
        <Card className="border-border/50">  
          <CardHeader>  
            <div className="flex items-center justify-between">  
              <div>  
                <CardTitle>Attestation Log</CardTitle>  
                <CardDescription>Immutable record of governance actions</CardDescription>  
              </div>  
              <Button   
                size="sm"   
                className="gap-2"  
                onClick={handleLogAction}  
              >  
                <Zap className="h-4 w-4" />  
                Log Action  
              </Button>  
            </div>  
          </CardHeader>  
          <CardContent className="space-y-0">  
            <div className="space-y-1 divide-y divide-border/30">  
              {attestations.map((att) => (  
                <div   
                  key={att.id}  
                  className="py-3 first:pt-0 last:pb-0 flex items-start gap-3 hover:bg-card/50 px-0 transition-colors"  
                >  
                  <CheckCircle className="h-4 w-4 text-primary mt-1 flex-shrink-0" />  
                  <div className="flex-1 min-w-0 text-sm">  
                    <div className="flex items-center justify-between gap-2 mb-1">  
                      <div className="font-mono text-xs font-bold text-foreground">  
                        {att.action}  
                      </div>  
                      <span className="text-xs text-muted-foreground">{att.timestamp}</span>  
                    </div>  
                    <div className="flex items-center gap-2 flex-wrap">  
                      <code className="text-xs bg-card/80 px-2 py-1 rounded font-mono text-accent">  
                        {att.hash.slice(0, 16)}...  
                      </code>  
                      <span className="text-xs text-muted-foreground">{att.userId}</span>  
                    </div>  
                  </div>  
                </div>  
              ))}  
            </div>  
          </CardContent>  
        </Card>  
  
        <Card className="border-border/50">  
          <CardHeader>  
            <CardTitle>System Operations</CardTitle>  
            <CardDescription>Real-time protocol activity</CardDescription>  
          </CardHeader>  
          <CardContent>  
            <div className="bg-card/50 rounded-lg border border-border/30 p-4 font-mono text-xs space-y-1 max-h-64 overflow-y-auto">  
              {logs.map((log, idx) => (  
                <div key={idx} className="text-muted-foreground hover:text-foreground transition-colors">  
                  <span className="text-primary">&gt;</span> {log}  
                </div>  
              ))}  
            </div>  
          </CardContent>  
        </Card>  
  
        <div className="space-y-6">  
          <h2 className="text-2xl font-bold tracking-tight">Universal Applications</h2>  
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">  
            {[  
              { title: "Healthcare", desc: "Clinical AI decisions audit trail" },  
              { title: "Finance", desc: "Trading and lending accountability" },  
              { title: "Public Sector", desc: "Government AI governance" },  
              { title: "Enterprise", desc: "Corporate AI compliance" }  
            ].map((use, idx) => (  
              <Card key={idx} className="border-border/50">  
                <CardHeader className="pb-3">  
                  <CardTitle className="text-sm">{use.title}</CardTitle>  
                </CardHeader>  
                <CardContent className="text-xs text-muted-foreground">  
                  {use.desc}  
                </CardContent>  
              </Card>  
            ))}  
          </div>  
        </div>  
  
        <div className="border-t border-border/30 pt-12 pb-12">  
          <div className="space-y-4 text-center">  
            <h3 className="text-2xl font-bold">Ready to Make AI Accountable?</h3>  
            <p className="text-muted-foreground max-w-2xl mx-auto">  
              Deploy GSP across your AI systems today. Universal governance, portable attestations, cryptographic accountability.  
            </p>  
            <div className="flex justify-center gap-4">  
              <Button className="gap-2">  
                Get Started  
              </Button>  
              <Button variant="outline">  
                Learn More  
              </Button>  
            </div>  
          </div>  
        </div>  
      </div>  
    </div>  
  );  
}  
  
# ++==Front end Auth Page (src/pages/auth.tsx)==++  
  
import { useState } from "react";  
import { useLocation } from "wouter";  
import { Button } from "@/components/ui/button";  
import { Input } from "@/components/ui/input";  
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";  
import { Lock, Mail, AlertCircle } from "lucide-react";  
  
export default function AuthPage() {  
  const [, navigate] = useLocation();  
  const [isLogin, setIsLogin] = useState(true);  
  const [email, setEmail] = useState("");  
  const [password, setPassword] = useState("");  
  const [error, setError] = useState("");  
  const [loading, setLoading] = useState(false);  
  
  const handleSubmit = async (e: React.FormEvent) => {  
    e.preventDefault();  
    setError("");  
    setLoading(true);  
  
    try {  
      const endpoint = isLogin ? "/api/auth/login" : "/api/auth/register";  
      const response = await fetch(endpoint, {  
        method: "POST",  
        headers: { "Content-Type": "application/json" },  
        body: JSON.stringify({ email, password }),  
      });  
  
      if (!response.ok) {  
        const data = await response.json();  
        throw new Error(data.error || "Authentication failed");  
      }  
  
      const data = await response.json();  
      localStorage.setItem("gsp_token", data.token);  
      navigate("/dashboard");  
    } catch (err) {  
      setError(err instanceof Error ? err.message : "Something went wrong");  
    } finally {  
      setLoading(false);  
    }  
  };  
  
  return (  
    <div className="min-h-screen bg-background text-foreground flex items-center justify-center p-4">  
      <Card className="w-full max-w-md border-border/50">  
        <CardHeader className="space-y-2">  
          <div className="flex items-center gap-2 mb-4">  
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center">  
              <Lock className="h-5 w-5 text-primary-foreground" />  
            </div>  
            <CardTitle>GSP Protocol</CardTitle>  
          </div>  
          <CardDescription>  
            {isLogin ? "Sign in to your account" : "Create a new account"}  
          </CardDescription>  
        </CardHeader>  
        <CardContent>  
          <form onSubmit={handleSubmit} className="space-y-4">  
            {error && (  
              <div className="flex items-start gap-3 p-3 rounded-lg bg-destructive/10 border border-destructive/20">  
                <AlertCircle className="h-4 w-4 text-destructive mt-0.5 flex-shrink-0" />  
                <p className="text-sm text-destructive">{error}</p>  
              </div>  
            )}  
  
            <div className="space-y-2">  
              <label className="text-sm font-medium">Email</label>  
              <div className="relative">  
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />  
                <Input  
                  type="email"  
                  placeholder="you@example.com"  
                  value={email}  
                  onChange={(e) => setEmail(e.target.value)}  
                  disabled={loading}  
                  className="pl-10"  
                  data-testid="input-email"  
                  required  
                />  
              </div>  
            </div>  
  
            <div className="space-y-2">  
              <label className="text-sm font-medium">Password</label>  
              <div className="relative">  
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />  
                <Input  
                  type="password"  
                  placeholder="••••••••"  
                  value={password}  
                  onChange={(e) => setPassword(e.target.value)}  
                  disabled={loading}  
                  className="pl-10"  
                  data-testid="input-password"  
                  required  
                />  
              </div>  
            </div>  
  
            <Button  
              type="submit"  
              disabled={loading}  
              className="w-full"  
              data-testid={`button-${isLogin ? "login" : "register"}`}  
            >  
              {loading ? "Processing..." : isLogin ? "Sign In" : "Create Account"}  
            </Button>  
          </form>  
  
          <div className="mt-6 pt-6 border-t border-border/30 text-center">  
            <p className="text-sm text-muted-foreground mb-3">  
              {isLogin ? "Don't have an account?" : "Already have an account?"}  
            </p>  
            <Button  
              variant="ghost"  
              onClick={() => {  
                setIsLogin(!isLogin);  
                setError("");  
              }}  
              className="w-full text-primary hover:text-primary"  
              data-testid={`button-toggle-${isLogin ? "register" : "login"}`}  
            >  
              {isLogin ? "Create one" : "Sign in instead"}  
            </Button>  
          </div>  
        </CardContent>  
      </Card>  
    </div>  
  );  
}  
  
# ++==Front end- Dashboard (src/pages/dashboard-gsp.tsx)==++  
  
import { useState, useEffect } from "react";  
import { useLocation } from "wouter";  
import { Button } from "@/components/ui/button";  
import { Input } from "@/components/ui/input";  
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";  
import { LogOut, Plus, CheckCircle, Clock, AlertCircle } from "lucide-react";  
  
interface Receipt {  
  id: number;  
  model_id: string;  
  input_hash: string;  
  output_hash: string;  
  policy_id: string;  
  attestation: Record<string, unknown>;  
  created_at: string;  
}  
  
export default function DashboardGSP() {  
  const [, navigate] = useLocation();  
  const [user, setUser] = useState<{ email: string } | null>(null);  
  const [receipts, setReceipts] = useState<Receipt[]>([]);  
  const [loading, setLoading] = useState(false);  
  const [error, setError] = useState("");  
  const [success, setSuccess] = useState("");  
    
  const [formData, setFormData] = useState({  
    modelId: "",  
    inputHash: "",  
    outputHash: "",  
    policyId: "",  
  });  
  
  const token = localStorage.getItem("gsp_token");  
  
  useEffect(() => {  
    if (!token) {  
      navigate("/auth");  
      return;  
    }  
    loadReceipts();  
  }, [token]);  
  
  const loadReceipts = async () => {  
    try {  
      const response = await fetch("/api/gsp/receipts", {  
        headers: { Authorization: `Bearer ${token}` },  
      });  
      if (response.ok) {  
        const data = await response.json();  
        setReceipts(data.receipts || []);  
        setUser(data.user);  
      } else if (response.status === 401) {  
        localStorage.removeItem("gsp_token");  
        navigate("/auth");  
      }  
    } catch (err) {  
      console.error("Failed to load receipts", err);  
    }  
  };  
  
  const handleSubmit = async (e: React.FormEvent) => {  
    e.preventDefault();  
    setError("");  
    setSuccess("");  
    setLoading(true);  
  
    try {  
      const response = await fetch("/api/gsp/submit", {  
        method: "POST",  
        headers: {  
          "Content-Type": "application/json",  
          Authorization: `Bearer ${token}`,  
        },  
        body: JSON.stringify(formData),  
      });  
  
      if (!response.ok) {  
        const data = await response.json();  
        throw new Error(data.error || "Submission failed");  
      }  
  
      const data = await response.json();  
      setSuccess(`Receipt created: #${data.receiptId}`);  
      setFormData({ modelId: "", inputHash: "", outputHash: "", policyId: "" });  
      await loadReceipts();  
    } catch (err) {  
      setError(err instanceof Error ? err.message : "Submission failed");  
    } finally {  
      setLoading(false);  
    }  
  };  
  
  const handleLogout = () => {  
    localStorage.removeItem("gsp_token");  
    navigate("/auth");  
  };  
  
  return (  
    <div className="min-h-screen bg-background text-foreground">  
      <header className="border-b border-border/30 bg-card/50 sticky top-0 z-10">  
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">  
          <div className="flex items-center gap-2">  
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center">  
              <span className="font-bold text-primary-foreground text-sm">GS</span>  
            </div>  
            <h1 className="font-display font-bold text-xl">GSP Dashboard</h1>  
          </div>  
          <div className="flex items-center gap-4">  
            <span className="text-sm text-muted-foreground hidden sm:inline">{user?.email}</span>  
            <Button  
              variant="outline"  
              size="sm"  
              onClick={handleLogout}  
              className="gap-2"  
              data-testid="button-logout"  
            >  
              <LogOut className="h-4 w-4" />  
              <span className="hidden sm:inline">Logout</span>  
            </Button>  
          </div>  
        </div>  
      </header>  
  
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8 space-y-8">  
        <Card className="border-border/50">  
          <CardHeader>  
            <CardTitle className="flex items-center gap-2">  
              <Plus className="h-5 w-5" />  
              Submit Inference Receipt  
            </CardTitle>  
            <CardDescription>  
              Log a new model inference with policy attestation  
            </CardDescription>  
          </CardHeader>  
          <CardContent>  
            <form onSubmit={handleSubmit} className="space-y-4">  
              {error && (  
                <div className="flex items-start gap-3 p-3 rounded-lg bg-destructive/10 border border-destructive/20">  
                  <AlertCircle className="h-4 w-4 text-destructive mt-0.5 flex-shrink-0" />  
                  <p className="text-sm text-destructive">{error}</p>  
                </div>  
              )}  
  
              {success && (  
                <div className="flex items-start gap-3 p-3 rounded-lg bg-primary/10 border border-primary/20">  
                  <CheckCircle className="h-4 w-4 text-primary mt-0.5 flex-shrink-0" />  
                  <p className="text-sm text-primary">{success}</p>  
                </div>  
              )}  
  
              <div className="grid gap-4 sm:grid-cols-2">  
                <div>  
                  <label className="text-sm font-medium block mb-2">Model ID</label>  
                  <Input  
                    placeholder="gpt4-v1"  
                    value={formData.modelId}  
                    onChange={(e) => setFormData({ ...formData, modelId: e.target.value })}  
                    disabled={loading}  
                    data-testid="input-modelId"  
                    required  
                  />  
                </div>  
                <div>  
                  <label className="text-sm font-medium block mb-2">Policy ID</label>  
                  <Input  
                    placeholder="policy-safety-v2"  
                    value={formData.policyId}  
                    onChange={(e) => setFormData({ ...formData, policyId: e.target.value })}  
                    disabled={loading}  
                    data-testid="input-policyId"  
                    required  
                  />  
                </div>  
                <div>  
                  <label className="text-sm font-medium block mb-2">Input Hash</label>  
                  <Input  
                    placeholder="0x..."  
                    value={formData.inputHash}  
                    onChange={(e) => setFormData({ ...formData, inputHash: e.target.value })}  
                    disabled={loading}  
                    data-testid="input-inputHash"  
                    required  
                  />  
                </div>  
                <div>  
                  <label className="text-sm font-medium block mb-2">Output Hash</label>  
                  <Input  
                    placeholder="0x..."  
                    value={formData.outputHash}  
                    onChange={(e) => setFormData({ ...formData, outputHash: e.target.value })}  
                    disabled={loading}  
                    data-testid="input-outputHash"  
                    required  
                  />  
                </div>  
              </div>  
  
              <Button type="submit" disabled={loading} className="w-full" data-testid="button-submit">  
                {loading ? "Submitting..." : "Submit Receipt"}  
              </Button>  
            </form>  
          </CardContent>  
        </Card>  
  
        <Card className="border-border/50">  
          <CardHeader>  
            <CardTitle>Recent Receipts</CardTitle>  
            <CardDescription>{receipts.length} total submissions</CardDescription>  
          </CardHeader>  
          <CardContent>  
            {receipts.length === 0 ? (  
              <div className="text-center py-12">  
                <Clock className="h-12 w-12 text-muted-foreground/30 mx-auto mb-4" />  
                <p className="text-muted-foreground">No receipts yet. Submit your first inference above.</p>  
              </div>  
            ) : (  
              <div className="space-y-3 divide-y divide-border/30">  
                {receipts.map((receipt) => (  
                  <div key={receipt.id} className="py-4 first:pt-0 last:pb-0">  
                    <div className="flex items-start justify-between gap-4 mb-3">  
                      <div className="flex-1">  
                        <div className="font-mono font-bold text-sm text-primary mb-1">  
                          Receipt #{receipt.id}  
                        </div>  
                        <div className="space-y-1 text-sm">  
                          <div className="flex items-center justify-between">  
                            <span className="text-muted-foreground">Model:</span>  
                            <code className="text-xs bg-card/80 px-2 py-1 rounded">  
                              {receipt.model_id}  
                            </code>  
                          </div>  
                          <div className="flex items-center justify-between">  
                            <span className="text-muted-foreground">Policy:</span>  
                            <code className="text-xs bg-card/80 px-2 py-1 rounded">  
                              {receipt.policy_id}  
                            </code>  
                          </div>  
                        </div>  
                      </div>  
                      <CheckCircle className="h-5 w-5 text-primary flex-shrink-0 mt-1" />  
                    </div>  
                    <details className="text-xs text-muted-foreground cursor-pointer hover:text-foreground transition-colors">  
                      <summary>Attestation Details</summary>  
                      <pre className="mt-2 p-2 rounded bg-card/50 overflow-x-auto">  
                        {JSON.stringify(receipt.attestation, null, 2)}  
                      </pre>  
                    </details>  
                    <div className="text-xs text-muted-foreground mt-2">  
                      {new Date(receipt.created_at).toLocaleString()}  
                    </div>  
                  </div>  
                ))}  
              </div>  
            )}  
          </CardContent>  
        </Card>  
      </div>  
    </div>  
  );  
}  
  
# ++==Backend- Express Server(server.js)==++  
  
import express from "express";  
import cors from "cors";  
import dotenv from "dotenv";  
import sqlite3 from "sqlite3";  
import bcrypt from "bcryptjs";  
import jwt from "jsonwebtoken";  
  
dotenv.config();  
  
const PORT = Number(process.env.PORT || 4000);  
const DB_PATH = process.env.DB_PATH || "./gsp.sqlite";  
const JWT_SECRET = process.env.JWT_SECRET || "change-me";  
const APP_NAME = process.env.APP_NAME || "GSP Reference App";  
const ATTESTATION_MODE = process.env.ATTESTATION_MODE || "simulated";  
  
const app = express();  
app.use(cors());  
app.use(express.json({ limit: "1mb" }));  
  
/* SQLite init */  
sqlite3.verbose();  
const db = new sqlite3.Database(DB_PATH);  
  
function nowISO() {  
  return new Date().toISOString();  
}  
  
db.serialize(() => {  
  db.run(`  
    CREATE TABLE IF NOT EXISTS users (  
      id INTEGER PRIMARY KEY AUTOINCREMENT,  
      email TEXT UNIQUE NOT NULL,  
      password_hash TEXT NOT NULL,  
      created_at TEXT NOT NULL  
    )  
  `);  
  
  db.run(`  
    CREATE TABLE IF NOT EXISTS receipts (  
      id INTEGER PRIMARY KEY AUTOINCREMENT,  
      user_id INTEGER NOT NULL,  
      model_id TEXT NOT NULL,  
      input_hash TEXT NOT NULL,  
      output_hash TEXT NOT NULL,  
      policy_id TEXT NOT NULL,  
      attestation TEXT NOT NULL,  
      created_at TEXT NOT NULL,  
      FOREIGN KEY(user_id) REFERENCES users(id)  
    )  
  `);  
});  
  
/* Auth middleware */  
function requireAuth(req, res, next) {  
  const header = req.headers.authorization || "";  
  const token = header.startsWith("Bearer ") ? header.slice(7) : null;  
  
  if (!token) return res.status(401).json({ error: "Missing Bearer token" });  
  
  try {  
    const decoded = jwt.verify(token, JWT_SECRET);  
    req.user = { id: decoded.sub, email: decoded.email };  
    return next();  
  } catch {  
    return res.status(401).json({ error: "Invalid token" });  
  }  
}  
  
/* Attestation stub */  
function buildAttestation({ userId, modelId, inputHash, outputHash, policyId }) {  
  return {  
    mode: ATTESTATION_MODE,  
    issued_at: nowISO(),  
    subject: {  
      user_id: String(userId),  
      model_id: String(modelId),  
      policy_id: String(policyId),  
    },  
    hashes: { input: String(inputHash), output: String(outputHash) },  
    statement:  
      "Simulated attestation. Replace with real signing/TEE measurement + audit log anchoring.",  
  };  
}  
  
/* Routes */  
app.get("/health", (_req, res) => {  
  res.json({ ok: true, app: APP_NAME, time: nowISO() });  
});  
  
app.post("/api/auth/register", (req, res) => {  
  const { email, password } = req.body || {};  
  if (!email || !password) {  
    return res.status(400).json({ error: "email and password required" });  
  }  
  
  const createdAt = nowISO();  
  const passwordHash = bcrypt.hashSync(password, 10);  
  
  const stmt = db.prepare(  
    "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)"  
  );  
  
  stmt.run([String(email).toLowerCase(), passwordHash, createdAt], function (err) {  
    if (err) {  
      if (String(err.message || "").includes("UNIQUE")) {  
        return res.status(409).json({ error: "User already exists" });  
      }  
      return res.status(500).json({ error: "DB error", details: err.message });  
    }  
  
    return res.json({  
      ok: true,  
      user: { id: this.lastID, email: String(email).toLowerCase(), created_at: createdAt },  
    });  
  });  
});  
  
app.post("/api/auth/login", (req, res) => {  
  const { email, password } = req.body || {};  
  if (!email || !password) {  
    return res.status(400).json({ error: "email and password required" });  
  }  
  
  db.get(  
    "SELECT id, email, password_hash FROM users WHERE email = ?",  
    [String(email).toLowerCase()],  
    (err, row) => {  
      if (err) return res.status(500).json({ error: "DB error", details: err.message });  
      if (!row) return res.status(401).json({ error: "Invalid credentials" });  
  
      const ok = bcrypt.compareSync(password, row.password_hash);  
      if (!ok) return res.status(401).json({ error: "Invalid credentials" });  
  
      const token = jwt.sign({ email: row.email }, JWT_SECRET, {  
        subject: String(row.id),  
        expiresIn: "7d",  
      });  
  
      return res.json({ ok: true, token });  
    }  
  );  
});  
  
app.post("/api/gsp/submit", requireAuth, (req, res) => {  
  const { modelId, inputHash, outputHash, policyId } = req.body || {};  
  if (!modelId || !inputHash || !outputHash || !policyId) {  
    return res.status(400).json({  
      error: "modelId, inputHash, outputHash, policyId are required",  
    });  
  }  
  
  const createdAt = nowISO();  
  const attestation = buildAttestation({  
    userId: req.user.id,  
    modelId,  
    inputHash,  
    outputHash,  
    policyId,  
  });  
  
  const stmt = db.prepare(`  
    INSERT INTO receipts  
      (user_id, model_id, input_hash, output_hash, policy_id, attestation, created_at)  
    VALUES (?, ?, ?, ?, ?, ?, ?)  
  `);  
  
  stmt.run(  
    [  
      req.user.id,  
      String(modelId),  
      String(inputHash),  
      String(outputHash),  
      String(policyId),  
      JSON.stringify(attestation),  
      createdAt,  
    ],  
    function (err) {  
      if (err) return res.status(500).json({ error: "DB error", details: err.message });  
      return res.json({ ok: true, receiptId: this.lastID, createdAt });  
    }  
  );  
});  
  
app.get("/api/gsp/receipt/:id", requireAuth, (req, res) => {  
  const id = Number(req.params.id);  
  
  db.get(  
    "SELECT * FROM receipts WHERE id = ? AND user_id = ?",  
    [id, req.user.id],  
    (err, row) => {  
      if (err) return res.status(500).json({ error: "DB error", details: err.message });  
      if (!row) return res.status(404).json({ error: "Receipt not found" });  
  
      let attestation = null;  
      try {  
        attestation = JSON.parse(row.attestation);  
      } catch {  
        attestation = row.attestation;  
      }  
  
      return res.json({  
        ok: true,  
        receipt: {  
          id: row.id,  
          user_id: row.user_id,  
          model_id: row.model_id,  
          input_hash: row.input_hash,  
          output_hash: row.output_hash,  
          policy_id: row.policy_id,  
          attestation,  
          created_at: row.created_at,  
        },  
      });  
    }  
  );  
});  
  
app.get("/api/gsp/receipts", requireAuth, (req, res) => {  
  db.all(  
    "SELECT * FROM receipts WHERE user_id = ? ORDER BY created_at DESC",  
    [req.user.id],  
    (err, rows) => {  
      if (err) return res.status(500).json({ error: "DB error", details: err.message });  
  
      const receipts = (rows || []).map(row => ({  
        ...row,  
        attestation: JSON.parse(row.attestation || "{}")  
      }));  
  
      return res.json({  
        ok: true,  
        user: { email: req.user.email },  
        receipts,  
      });  
    }  
  );  
});  
  
app.listen(PORT, () => {  
  console.log(`${APP_NAME} backend running on http://0.0.0.0:${PORT}`);  
});  
  
# ++==Backend .env==++  
  
PORT=4000  
DB_PATH=./gsp.sqlite  
JWT_SECRET=your-super-secret-key-change-this  
APP_NAME=GSP Reference App  
ATTESTATION_MODE=simulated  
  
  
# ++==Backend package.json==++  
  
{  
  "name": "gsp-backend",  
  "type": "module",  
  "version": "1.0.0",  
  "scripts": {  
    "dev": "node server.js",  
    "start": "node server.js"  
  },  
  "dependencies": {  
    "express": "^4.19.2",  
    "cors": "^2.8.5",  
    "dotenv": "^16.4.5",  
    "sqlite3": "^5.1.7",  
    "bcryptjs": "^2.4.3",  
    "jsonwebtoken": "^9.0.2"  
  }  
}  
  
# ++==Backend server==++  
npm install  
node server.js  
  
**>>> connect frontend to backend by using: **VITE_API_BASE=http://your-backend-url:4000  
  
