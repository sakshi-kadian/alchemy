
"use client";

import React, { useRef, useEffect } from 'react';
import dynamic from 'next/dynamic';

// Dynamic import to avoid SSR issues
const ForceGraph2D = dynamic(
    () => import('react-force-graph-2d'),
    { ssr: false }
);

interface GraphData {
    nodes: Array<{ id: string; type: string; label: string }>;
    links: Array<{ source: string; target: string }>;
}

export default function GraphVisualization({ graphData }: { graphData: GraphData }) {
    const fgRef = useRef<any>(null);
    return (
        <div className="w-full h-full relative">


            {graphData && graphData.nodes.length > 0 ? (
                <ForceGraph2D
                    ref={fgRef}
                    graphData={graphData}
                    nodeLabel="label"
                    nodeColor={(node: any) => {
                        if (node.type === 'toxicity') return '#ef4444'; // Red-500 (Risk)
                        if (node.type === 'mechanism') return '#10b981'; // Emerald-500 (Target)
                        if (node.type === 'molecule') return '#ffffff'; // White (Drug)
                        return '#525252'; // Neutral-600 (Context)
                    }}
                    nodeRelSize={6}
                    linkColor={() => '#ffffff40'}
                    linkWidth={1.5}
                    backgroundColor="#00000000"
                    nodeCanvasObject={(node: any, ctx, globalScale) => {
                        const label = node.label;
                        const fontSize = 12 / globalScale;
                        ctx.font = `${fontSize}px Sans-Serif`;
                        const textWidth = ctx.measureText(label).width;
                        const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding

                        ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
                        ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, bckgDimensions[0], bckgDimensions[1]);

                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';

                        // Node Body
                        ctx.fillStyle = node.color || '#94a3b8';
                        ctx.beginPath();
                        ctx.arc(node.x, node.y, 5, 0, 2 * Math.PI, false);
                        ctx.fill();

                        // Node Label
                        ctx.fillStyle = '#ffffff';
                        ctx.fillText(label, node.x, node.y + 8);
                    }}
                    cooldownTicks={100}
                    onEngineStop={() => fgRef.current.zoomToFit(400)}
                />
            ) : (
                <div className="flex items-center justify-center h-full text-zinc-500 text-sm">
                    Generate a candidate to trace reasoning paths.
                </div>
            )}
        </div>
    );
}
