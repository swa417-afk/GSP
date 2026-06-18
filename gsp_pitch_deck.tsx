import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, Shield, Lock, Database, CheckCircle, TrendingUp, Users, Zap, Target, Award } from 'lucide-react';

const PitchDeck = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    {
      type: 'title',
      title: 'Glass Substrate Protocol',
      subtitle: 'The Trust Layer for AI Systems',
      tagline: '5 Access Entrepreneur Opportunity',
      founder: 'Sierra Warren',
      background: 'linear-gradient(135deg, #1E57C0 0%, #0F132F 100%)'
    },
    {
      type: 'hook',
      title: 'The Problem',
      headline: 'AI is making decisions that affect millions of lives—but nobody knows who to blame when it goes wrong.',
      scenarios: [
        'AI denies your loan application',
        'Autonomous system makes a critical error',
        'Algorithm discriminates in hiring',
        'Medical AI misdiagnoses a patient'
      ],
      question: 'Who is responsible? The user? The developer? The AI itself?'
    },
    {
      type: 'solution',
      title: 'The Solution: GSP',
      tagline: 'Every AI decision gets a cryptographic receipt',
      description: 'GSP is middleware that creates immutable audit trails for AI systems—like a blockchain for AI accountability.',
      analogy: 'Think: "Flight recorder for AI" meets "Notary public for algorithms"',
      keyFeatures: [
        'Hardware-enforced cryptographic logging',
        'Real-time ethical governance layer',
        'Automatic fault attribution',
        'No model retraining required'
      ]
    },
    {
      type: 'demo',
      title: 'How It Works',
      steps: [
        {
          step: '1',
          icon: Zap,
          title: 'AI makes decision',
          description: 'System processes user input through AI model'
        },
        {
          step: '2',
          icon: Lock,
          title: 'GSP intercepts',
          description: 'Middleware captures context, parameters, and reasoning'
        },
        {
          step: '3',
          icon: Shield,
          title: 'Creates attestation',
          description: 'SHA-256 hash generates immutable "moral receipt"'
        },
        {
          step: '4',
          icon: Database,
          title: 'Stores proof',
          description: 'Cryptographic record enables full reconstruction'
        }
      ],
      cta: 'Working prototype available for demo'
    },
    {
      type: 'traction',
      title: 'Current Progress',
      items: [
        { 
          icon: CheckCircle, 
          text: 'Functional prototype with cryptographic attestation system',
          metric: 'Built'
        },
        { 
          icon: Award, 
          text: 'Patent pending on core architecture',
          metric: 'Filed'
        },
        { 
          icon: CheckCircle, 
          text: 'Research validated through academic coursework',
          metric: 'Validated'
        },
        { 
          icon: TrendingUp, 
          text: '3 trademark applications (GSP, G-BALO, Sierra Certified)',
          metric: 'In Process'
        },
        { 
          icon: Users, 
          text: 'Interest from federal contractor community',
          metric: 'Early signals'
        }
      ]
    },
    {
      type: 'market',
      title: 'Market Opportunity',
      total: '$180B+ AI Governance Market',
      segments: [
        {
          name: 'Enterprise AI Compliance',
          size: '$45B',
          growth: '32% CAGR',
          use: 'HR, finance, operations'
        },
        {
          name: 'Government & Defense',
          size: '$28B',
          growth: '28% CAGR',
          use: 'Intelligence, autonomous systems'
        },
        {
          name: 'Healthcare AI',
          size: '$67B',
          growth: '41% CAGR',
          use: 'Diagnostics, treatment decisions'
        },
        {
          name: 'Financial Services',
          size: '$40B',
          growth: '35% CAGR',
          use: 'Fraud detection, credit decisions'
        }
      ]
    },
    {
      type: 'business_model',
      title: 'Revenue Model',
      streams: [
        {
          name: 'SaaS Licensing',
          description: 'Per-transaction or per-seat pricing for enterprise deployments',
          pricing: '$0.001 - $0.10 per attestation',
          target: 'Enterprise customers'
        },
        {
          name: 'Sierra Certified™',
          description: 'Certification program for third-party AI systems',
          pricing: '$25K - $250K per certification',
          target: 'AI vendors & platforms'
        },
        {
          name: 'Implementation Services',
          description: 'Custom integration and consulting',
          pricing: '$150K - $500K per engagement',
          target: 'Government & Fortune 500'
        }
      ]
    },
    {
      type: 'competitive',
      title: 'Why GSP Wins',
      advantages: [
        {
          feature: 'Hardware-enforced',
          competitors: 'Software logs (can be altered)',
          gsp: 'Cryptographically immutable'
        },
        {
          feature: 'No retraining needed',
          competitors: 'Requires model modification',
          gsp: 'Middleware layer—plug & play'
        },
        {
          feature: 'Real-time governance',
          competitors: 'Post-hoc auditing only',
          gsp: 'Active ethical enforcement'
        },
        {
          feature: 'Fault attribution',
          competitors: 'Manual investigation',
          gsp: 'Automatic liability mapping'
        }
      ]
    },
    {
      type: 'ask',
      title: 'The Ask',
      request: 'Seeking 5 Access Support',
      needs: [
        {
          category: 'Mentorship',
          items: [
            'Legal: IP strategy & patent prosecution',
            'Technical: Cloud architecture for scale',
            'Business: Enterprise sales strategy',
            'Regulatory: Federal procurement navigation'
          ]
        },
        {
          category: 'Network Access',
          items: [
            'Introductions to federal contractors',
            'Connections to AI ethics boards',
            'Enterprise CISO & compliance officer network',
            'Venture capital warm intros'
          ]
        },
        {
          category: 'Resources',
          items: [
            'Cloud credits for pilot deployments',
            'Legal support for trademark filings',
            'Marketing support for thought leadership',
            'Technical advisor for security audits'
          ]
        }
      ]
    },
    {
      type: 'milestones',
      title: 'Next 12 Months',
      timeline: [
        {
          quarter: 'Q1 2026',
          goals: [
            'Complete patent prosecution',
            'Finalize trademark registrations',
            'Launch beta program with 3 pilot customers'
          ]
        },
        {
          quarter: 'Q2 2026',
          goals: [
            'First Sierra Certified™ third-party system',
            'Federal contractor pilot deployment',
            'Publish peer-reviewed research paper'
          ]
        },
        {
          quarter: 'Q3 2026',
          goals: [
            'Scale to 10 enterprise customers',
            'Launch certification program',
            'Achieve $100K ARR'
          ]
        },
        {
          quarter: 'Q4 2026',
          goals: [
            'Series A fundraise preparation',
            'Expand to healthcare vertical',
            'Build out G-BALO advisory board'
          ]
        }
      ]
    },
    {
      type: 'founder',
      title: 'About the Founder',
      name: 'Sierra Warren',
      role: 'Founder & Protocol Architect',
      background: [
        'Ethical AI Governance Systems Engineer',
        'Creator of Glass Substrate Protocol architecture',
        'Founder of G-BALO (Governing Board for AI Liability Oversight)',
        'Academic research in AI trust, transparency, and accountability'
      ],
      vision: 'Building the infrastructure layer that makes AI systems trustworthy, explainable, and legally defensible.',
      commitment: 'Full-time dedicated to GSP development and commercialization'
    },
    {
      type: 'closing',
      title: 'The Vision',
      message: 'In 10 years, every high-stakes AI decision will come with a cryptographic proof of why it was made and who is responsible.',
      mission: 'GSP will be the standard—just like HTTPS became the standard for secure web traffic.',
      cta: 'Help me build the trust layer for the AI era.',
      contact: {
        name: 'Sierra Warren',
        subtitle: 'Glass Substrate Protocol',
        action: 'Let\'s talk about making AI accountable.'
      }
    }
  ];

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  const renderSlide = (slide) => {
    switch (slide.type) {
      case 'title':
        return (
          <div className="h-full flex flex-col items-center justify-center text-white p-12" style={{ background: slide.background }}>
            <div className="text-7xl font-bold mb-4">{slide.title}</div>
            <div className="text-3xl mb-6 opacity-90">{slide.subtitle}</div>
            <div className="text-xl mb-8 opacity-75 italic">{slide.tagline}</div>
            <div className="mt-8 text-2xl font-semibold">{slide.founder}</div>
          </div>
        );

      case 'hook':
        return (
          <div className="h-full p-12 bg-gradient-to-br from-red-50 to-orange-50">
            <h2 className="text-5xl font-bold mb-8 text-slate-800">{slide.title}</h2>
            <p className="text-2xl font-semibold text-red-600 mb-8 leading-relaxed">{slide.headline}</p>
            <div className="grid grid-cols-2 gap-4 mb-8">
              {slide.scenarios.map((scenario, idx) => (
                <div key={idx} className="bg-white p-6 rounded-lg shadow-md border-l-4 border-red-500">
                  <p className="text-lg text-slate-700">{scenario}</p>
                </div>
              ))}
            </div>
            <p className="text-3xl font-bold text-slate-800 mt-8">{slide.question}</p>
          </div>
        );

      case 'solution':
        return (
          <div className="h-full p-12 bg-gradient-to-br from-blue-50 to-indigo-50">
            <h2 className="text-5xl font-bold mb-4 text-slate-800">{slide.title}</h2>
            <p className="text-2xl font-semibold text-indigo-600 mb-6">{slide.tagline}</p>
            <p className="text-xl text-slate-700 mb-6">{slide.description}</p>
            <div className="bg-indigo-100 p-6 rounded-lg mb-6 border-l-4 border-indigo-600">
              <p className="text-xl italic text-indigo-900">{slide.analogy}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              {slide.keyFeatures.map((feature, idx) => (
                <div key={idx} className="flex items-center gap-3 bg-white p-4 rounded-lg shadow-sm">
                  <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0" />
                  <span className="text-lg text-slate-700">{feature}</span>
                </div>
              ))}
            </div>
          </div>
        );

      case 'demo':
        return (
          <div className="h-full p-12 bg-gradient-to-br from-slate-50 to-blue-50">
            <h2 className="text-5xl font-bold mb-12 text-slate-800">{slide.title}</h2>
            <div className="grid grid-cols-4 gap-4 mb-8">
              {slide.steps.map((step, idx) => (
                <div key={idx} className="text-center">
                  <div className="bg-white p-6 rounded-lg shadow-md mb-3 h-full">
                    <div className="text-4xl font-bold text-blue-200 mb-4">{step.step}</div>
                    <step.icon className="w-12 h-12 text-blue-600 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold mb-2 text-slate-800">{step.title}</h3>
                    <p className="text-sm text-slate-600">{step.description}</p>
                  </div>
                  {idx < slide.steps.length - 1 && (
                    <div className="text-blue-400 text-3xl">→</div>
                  )}
                </div>
              ))}
            </div>
            <div className="bg-green-100 p-4 rounded-lg text-center">
              <p className="text-xl font-semibold text-green-800">{slide.cta}</p>
            </div>
          </div>
        );

      case 'traction':
        return (
          <div className="h-full p-12 bg-gradient-to-br from-purple-50 to-pink-50">
            <h2 className="text-5xl font-bold mb-12 text-slate-800">{slide.title}</h2>
            <div className="space-y-5">
              {slide.items.map((item, idx) => (
                <div key={idx} className="flex items-center gap-6 bg-white p-6 rounded-lg shadow-md">
                  <item.icon className="w-10 h-10 text-purple-600 flex-shrink-0" />
                  <div className="flex-1">
                    <p className="text-lg text-slate-700">{item.text}</p>
                  </div>
                  <div className="bg-purple-100 px-4 py-2 rounded-full">
                    <span className="text-sm font-semibold text-purple-800">{item.metric}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        );

      case 'market':
        return (
          <div className="h-full p-12 bg-gradient-to-br from-green-50 to-emerald-50">
            <h2 className="text-5xl font-bold mb-4 text-slate-800">{slide.title}</h2>
            <p className="text-3xl font-bold text-green-600 mb-8">{slide.total}</p>
            <div className="grid grid-cols-2 gap-6">
              {slide.segments.map((segment, idx) => (
                <div key={idx} className="bg-white p-6 rounded-lg shadow-md">
                  <h3 className="text-xl font-semibold mb-2 text-slate-800">{segment.name}</h3>
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-3xl font-bold text-green-600">{segment.size}</span>
                    <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
                      {segment.growth}
                    </span>
                  </div>
                  <p className="text-slate-600">{segment.use}</p>
                </div>
              ))}
            </div>
          </div>
        );

      case 'business_model':
        return (
          <div className="h-full p-12 bg-gradient-to-br from-amber-50 to-orange-50">
            <h2 className="text-5xl font-bold mb-12 text-slate-800">{slide.title}</h2>
            <div className="space-y-6">
              {slide.streams.map((stream, idx) => (
                <div key={idx} className="bg-white p-6 rounded-lg shadow-md">
                  <div className="flex justify-between items-start mb-3">
                    <h3 className="text-2xl font-semibold text-slate-800">{stream.name}</h3>
                    <span className="bg-amber-100 text-amber-800 px-3 py-1 rounded-full text-sm font-medium">
                      {stream.target}
                    </span>
                  </div>
                  <p className="text-slate-700 mb-2">{stream.description}</p>
                  <p className="text-lg font-semibold text-green-600">{stream.pricing}</p>
                </div>
              ))}
            </div>
          </div>
        );

      case 'competitive':
        return (
          <div className="h-full p-12 bg-gradient-to-br from-cyan-50 to-blue-50">
            <h2 className="text-5xl font-bold mb-12 text-slate-800">{slide.title}</h2>
            <div className="space-y-4">
              {slide.advantages.map((adv, idx) => (
                <div key={idx} className="bg-white p-5 rounded-lg shadow-md">
                  <div className="grid grid-cols-3 gap-4 items-center">
                    <div className="font-semibold text-lg text-slate-800">{adv.feature}</div>
                    <div className="text-slate-600">❌ {adv.competitors}</div>
                    <div className="text-green-600 font-semibold">✅ {adv.gsp}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        );

      case 'ask':
        return (
          <div className="h-full p-12 bg-gradient-to-br from-indigo-50 to-purple-50">
            <h2 className="text-5xl font-bold mb-4 text-slate-800">{slide.title}</h2>
            <p className="text-2xl font-semibold text-indigo-600 mb-8">{slide.request}</p>
            
            <div className="grid grid-cols-3 gap-6">
              {slide.needs.map((need, idx) => (
                <div key={idx} className="bg-white p-6 rounded-lg shadow-md">
                  <h3 className="text-xl font-semibold mb-4 text-slate-800 border-b-2 border-indigo-200 pb-2">
                    {need.category}
                  </h3>
                  <ul className="space-y-3">
                    {need.items.map((item, itemIdx) => (
                      <li key={itemIdx} className="flex items-start gap-2">
                        <Target className="w-5 h-5 text-indigo-600 flex-shrink-0 mt-0.5" />
                        <span className="text-slate-700">{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        );

      case 'milestones':
        return (
          <div className="h-full p-12 bg-gradient-to-br from-slate-50 to-slate-100">
            <h2 className="text-5xl font-bold mb-12 text-slate-800">{slide.title}</h2>
            <div className="grid grid-cols-2 gap-6">
              {slide.timeline.map((period, idx) => (
                <div key={idx} className="bg-white p-6 rounded-lg shadow-md">
                  <h3 className="text-2xl font-bold mb-4 text-indigo-600">{period.quarter}</h3>
                  <ul className="space-y-3">
                    {period.goals.map((goal, goalIdx) => (
                      <li key={goalIdx} className="flex items-start gap-3">
                        <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-0.5" />
                        <span className="text-slate-700">{goal}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        );

      case 'founder':
        return (
          <div className="h-full p-12 bg-gradient-to-br from-slate-50 to-blue-50">
            <h2 className="text-5xl font-bold mb-8 text-slate-800">{slide.title}</h2>
            
            <div className="bg-white p-8 rounded-lg shadow-md mb-6">
              <h3 className="text-3xl font-semibold mb-2 text-slate-800">{slide.name}</h3>
              <p className="text-xl text-indigo-600 mb-6">{slide.role}</p>
              
              <div className="space-y-3 mb-6">
                {slide.background.map((item, idx) => (
                  <div key={idx} className="flex items-start gap-3">
                    <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-0.5" />
                    <span className="text-slate-700">{item}</span>
                  </div>
                ))}
              </div>
              
              <div className="bg-indigo-50 p-6 rounded-lg mb-4 border-l-4 border-indigo-600">
                <p className="text-lg italic text-indigo-900">{slide.vision}</p>
              </div>
              
              <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-600">
                <p className="text-slate-800 font-semibold">{slide.commitment}</p>
              </div>
            </div>
          </div>
        );

      case 'closing':
        return (
          <div className="h-full flex flex-col items-center justify-center text-white p-12 bg-gradient-to-br from-indigo-900 to-purple-900">
            <h2 className="text-6xl font-bold mb-8">{slide.title}</h2>
            <p className="text-2xl mb-6 text-center max-w-4xl opacity-90 leading-relaxed">{slide.message}</p>
            <p className="text-xl mb-12 text-center max-w-3xl opacity-75 italic">{slide.mission}</p>
            <p className="text-2xl font-semibold mb-12">{slide.cta}</p>
            <div className="text-center">
              <div className="text-2xl font-bold mb-2">{slide.contact.name}</div>
              <div className="text-lg opacity-90 mb-4">{slide.contact.subtitle}</div>
              <div className="text-xl italic opacity-75">{slide.contact.action}</div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="w-full h-screen bg-slate-100 flex flex-col">
      <div className="flex-1 relative overflow-hidden">
        {renderSlide(slides[currentSlide])}
      </div>
      
      <div className="bg-white border-t border-slate-200 p-4 flex items-center justify-between">
        <button
          onClick={prevSlide}
          className="flex items-center gap-2 px-4 py-2 bg-slate-200 hover:bg-slate-300 rounded-lg transition-colors"
        >
          <ChevronLeft className="w-5 h-5" />
          Previous
        </button>
        
        <div className="flex gap-2">
          {slides.map((_, idx) => (
            <button
              key={idx}
              onClick={() => setCurrentSlide(idx)}
              className={`w-2 h-2 rounded-full transition-colors ${
                idx === currentSlide ? 'bg-indigo-600' : 'bg-slate-300'
              }`}
            />
          ))}
        </div>
        
        <button
          onClick={nextSlide}
          className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors"
        >
          Next
          <ChevronRight className="w-5 h-5" />
        </button>
      </div>
      
      <div className="bg-slate-800 text-white text-center py-2 text-sm">
        Slide {currentSlide + 1} of {slides.length} • 5 Access Pitch Deck
      </div>
    </div>
  );
};

export default PitchDeck;