import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { Maximize2, Minimize2 } from "lucide-react";
import { AgentState } from "@/lib/useExperiment";
import { NotebookCell } from "./NotebookCell";
import { StatusBadge } from "../StatusBadge";
import { cn } from "@/lib/utils";

interface AgentNotebookProps {
    agent: AgentState;
}

function AgentNotebookContent({ 
    agent, 
    isExpanded, 
    onToggleExpand, 
    isModal = false 
}: { 
    agent: AgentState;
    isExpanded: boolean;
    onToggleExpand: () => void;
    isModal?: boolean;
}) {
    const scrollRef = useRef<HTMLDivElement>(null);
    const autoScrollEnabledRef = useRef(true);
    const isProgrammaticScrollRef = useRef(false);
    const timeoutRef = useRef<NodeJS.Timeout | null>(null);

    const scrollToBottom = () => {
        if (scrollRef.current) {
            isProgrammaticScrollRef.current = true;
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
            // Small timeout to ensure the onScroll event fired by this change 
            // is ignored by our handler.
            setTimeout(() => {
                isProgrammaticScrollRef.current = false;
            }, 50);
        }
    };

    // Auto-scroll effect
    useEffect(() => {
        // We depend on the entire agent object to catch streaming updates
        if (autoScrollEnabledRef.current) {
            scrollToBottom();
        }
    }, [agent]);

    const handleScroll = () => {
        if (!scrollRef.current) return;

        // Ignore scroll events triggered by our auto-scroll
        if (isProgrammaticScrollRef.current) {
            return;
        }

        const { scrollTop, scrollHeight, clientHeight } = scrollRef.current;
        const isAtBottom = scrollHeight - scrollTop - clientHeight < 50;

        if (isAtBottom) {
            // User is at the bottom, resume auto-scroll
            autoScrollEnabledRef.current = true;
            if (timeoutRef.current) {
                clearTimeout(timeoutRef.current);
                timeoutRef.current = null;
            }
        } else {
            // User scrolled away
            autoScrollEnabledRef.current = false;
            
            // Set/Reset 10s timeout to resume auto-scroll
            if (timeoutRef.current) {
                clearTimeout(timeoutRef.current);
            }
            
            timeoutRef.current = setTimeout(() => {
                autoScrollEnabledRef.current = true;
                // Optional: snap back to bottom immediately when timer fires?
                // The requirement says "goes back to auto-scroll-to-bottom", 
                // which we interpret as re-enabling the behavior. 
                // We'll also snap to bottom to make it clear the mode is back.
                scrollToBottom();
            }, 10000);
        }
    };

    return (
        <div className={cn(
            "flex flex-col h-full border border-[#1d1d1f] bg-black/50 backdrop-blur-sm transition-all duration-500",
            isModal ? "border-0 bg-black/95" : ""
        )}>
            {/* Header - Ultra Minimal */}
            <div className="flex-shrink-0 h-12 px-4 border-b border-[#1d1d1f] flex items-center justify-between bg-black/50">
                <div className="flex items-center gap-3">
                    <span className="text-[10px] font-medium text-[#f5f5f7] tracking-widest uppercase">
                        Agent {agent.id}
                    </span>
                    <div className="w-[1px] h-3 bg-[#1d1d1f]" />
                    <span className="text-[10px] font-medium text-[#6e6e73] uppercase tracking-widest">
                        {agent.gpu || "CPU"}
                    </span>
                </div>
                <div className="flex items-center gap-3">
                    <StatusBadge status={agent.status} />
                    <button 
                        onClick={onToggleExpand}
                        className="p-1.5 hover:bg-[#1d1d1f] rounded-md transition-colors text-[#86868b] hover:text-white"
                    >
                        {isExpanded ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
                    </button>
                </div>
            </div>

            {/* Hypothesis - Clean & Typography focused */}
            {agent.hypothesis && (
                <div className="flex-shrink-0 p-4 border-b border-[#1d1d1f] bg-black">
                    <div className="text-[10px] font-medium text-[#424245] uppercase tracking-widest mb-2">
                        Objective
                    </div>
                    <div className={cn(
                        "text-xs text-[#86868b] font-light leading-relaxed",
                        !isExpanded && "line-clamp-2"
                    )}>
                        {agent.hypothesis}
                    </div>
                </div>
            )}

            {/* Notebook Content */}
            <div 
                ref={scrollRef}
                onScroll={handleScroll}
                className={cn(
                    "flex-1 overflow-y-auto p-4 custom-scrollbar scroll-smooth",
                    isModal && "px-8 md:px-16" // Extra padding in modal mode
                )}
            >
                <div className={cn(
                    "space-y-8",
                    isModal && "max-w-4xl mx-auto" // Centered content in modal
                )}>
                    {agent.steps.length === 0 ? (
                        <div className="h-full flex flex-col items-center justify-center min-h-[200px]">
                            <div className="w-1 h-1 rounded-full bg-[#333] mb-3" />
                            <span className="text-[10px] font-medium text-[#424245] uppercase tracking-widest">Initializing Environment</span>
                        </div>
                    ) : (
                        agent.steps.map((step) => (
                            <NotebookCell key={step.id} step={step} />
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}

export function AgentNotebook({ agent }: AgentNotebookProps) {
    const [isExpanded, setIsExpanded] = useState(false);

    // Effect to handle body scroll locking when expanded
    useEffect(() => {
        if (isExpanded) {
            document.body.style.overflow = "hidden";
        } else {
            document.body.style.overflow = "unset";
        }
        return () => {
            document.body.style.overflow = "unset";
        };
    }, [isExpanded]);

    return (
        <>
            {/* Default View */}
            <div className={cn("h-full", isExpanded && "invisible")}>
                <AgentNotebookContent 
                    agent={agent} 
                    isExpanded={isExpanded} 
                    onToggleExpand={() => setIsExpanded(!isExpanded)} 
                />
            </div>

            {/* Expanded Modal View */}
            {isExpanded && createPortal(
                <div className="fixed inset-0 z-[100] bg-black/80 backdrop-blur-md animate-in fade-in duration-200 p-4 md:p-8">
                    <div className="w-full h-full rounded-lg overflow-hidden animate-in zoom-in-95 duration-300 border border-[#1d1d1f] shadow-2xl">
                        <AgentNotebookContent 
                            agent={agent} 
                            isExpanded={isExpanded} 
                            onToggleExpand={() => setIsExpanded(!isExpanded)}
                            isModal={true} 
                        />
                    </div>
                </div>,
                document.body
            )}
        </>
    );
}
