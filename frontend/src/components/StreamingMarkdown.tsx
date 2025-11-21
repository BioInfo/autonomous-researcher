import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { cn } from "@/lib/utils";

interface StreamingMarkdownProps {
    content: string;
    wrapperClassName?: string;
    markdownClassName?: string;
}

/**
 * Markdown block that lightly fades in whenever its content changes.
 * This keeps streamed tokens feeling alive without re-mounting the whole row.
 */
export function StreamingMarkdown({ content, wrapperClassName, markdownClassName }: StreamingMarkdownProps) {
    const [isUpdating, setIsUpdating] = useState(false);
    const hasAnimatedRef = useRef(false);

    useEffect(() => {
        if (hasAnimatedRef.current) return;
        if (!content || content.length === 0) return;

        setIsUpdating(true);
        hasAnimatedRef.current = true;

        const timeout = window.setTimeout(() => setIsUpdating(false), 420);
        return () => window.clearTimeout(timeout);
    }, [content]);

    return (
        <div className={cn("stream-fade", isUpdating && "stream-fade--active", wrapperClassName, markdownClassName)}>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {content}
            </ReactMarkdown>
        </div>
    );
}
