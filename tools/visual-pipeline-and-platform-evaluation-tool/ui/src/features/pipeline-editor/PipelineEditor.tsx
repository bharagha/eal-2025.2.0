import {
  Background,
  BackgroundVariant,
  Controls,
  type Edge as ReactFlowEdge,
  type Node as ReactFlowNode,
  type NodeMouseHandler,
  Position,
  ReactFlow,
  useEdgesState,
  useNodesState,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { useEffect, useState } from "react";
import dagre from "dagre";
import {
  defaultNodeWidth,
  nodeTypes,
  nodeWidths,
} from "@/features/pipeline-editor/nodes";
import NodeDataPanel from "@/features/pipeline-editor/NodeDataPanel.tsx";
import { type Pipeline } from "@/api/api.generated";

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

const nodeHeight = 120;

// Function to get node width based on node type
const getNodeWidth = (nodeType: string): number =>
  nodeWidths[nodeType] || defaultNodeWidth;

const transformApiNodes = (apiNodes: ReactFlowNode[]): ReactFlowNode[] =>
  apiNodes.map((node) => ({
    ...node,
    type: node.type,
  }));

const getLayoutedElements = (
  nodes: ReactFlowNode[],
  edges: ReactFlowEdge[],
  direction = "LR",
) => {
  const isHorizontal = direction === "LR";
  dagreGraph.setGraph({ rankdir: direction });

  nodes.forEach((node) => {
    const currentNodeWidth = getNodeWidth(node.type || "default");
    dagreGraph.setNode(node.id, {
      width: currentNodeWidth,
      height: nodeHeight,
    });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  const layoutedNodes = nodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    const currentNodeWidth = getNodeWidth(node.type || "default");
    return {
      ...node,
      targetPosition: isHorizontal ? Position.Left : Position.Top,
      sourcePosition: isHorizontal ? Position.Right : Position.Bottom,
      position: {
        x: nodeWithPosition.x - currentNodeWidth / 2,
        y: nodeWithPosition.y - nodeHeight / 2,
      },
    };
  });

  return { nodes: layoutedNodes, edges };
};

interface PipelineEditorProps {
  pipelineData?: Pipeline;
  onNodesChange?: (nodes: ReactFlowNode[]) => void;
  onEdgesChange?: (edges: ReactFlowEdge[]) => void;
}

const PipelineEditor = ({
  pipelineData,
  onNodesChange: onNodesChangeCallback,
  onEdgesChange: onEdgesChangeCallback,
}: PipelineEditorProps) => {
  const [selectedNode, setSelectedNode] = useState<ReactFlowNode | null>(null);
  const [nodes, setNodes, onNodesChange] = useNodesState<ReactFlowNode>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<ReactFlowEdge>([]);

  // Handle node click to show data panel
  const onNodeClick: NodeMouseHandler = (event, node) => {
    event.stopPropagation();
    setSelectedNode(node);
  };

  // Handle background click to deselect node
  const onPaneClick = () => {
    setSelectedNode(null);
  };

  // Handle node data updates
  const handleNodeDataUpdate = (
    nodeId: string,
    updatedData: Record<string, unknown>,
  ) => {
    setNodes((currentNodes) => {
      const updatedNodes = currentNodes.map((node) =>
        node.id === nodeId ? { ...node, data: updatedData } : node,
      );
      // Notify parent component of nodes change
      onNodesChangeCallback?.(updatedNodes);
      return updatedNodes;
    });
  };

  // Notify parent when nodes or edges change
  useEffect(() => {
    onNodesChangeCallback?.(nodes);
  }, [nodes, onNodesChangeCallback]);

  useEffect(() => {
    onEdgesChangeCallback?.(edges);
  }, [edges, onEdgesChangeCallback]);

  useEffect(() => {
    if (pipelineData?.launch_config) {
      // const rawNodes = pipelineData.launch_config.nodes || [];
      // const rawEdges = pipelineData.launch_config.edges || [];
      // Get the raw nodes and edges from API (using hardcoded data for now)
      const rawNodes: ReactFlowNode[] = [
        {
          id: "0",
          type: "filesrc",
          data: {
            location: "${VIDEO}",
          },
          position: { x: 0, y: 0 },
        },
        {
          id: "1",
          type: "qtdemux",
          data: {},
          position: { x: 0, y: 0 },
        },
        {
          id: "2",
          type: "h264parse",
          data: {},
          position: { x: 0, y: 0 },
        },
        {
          id: "3",
          type: "vah264dec",
          data: {},
          position: { x: 0, y: 0 },
        },
        {
          id: "4",
          type: "video/x-raw(memory:VAMemory)",
          data: {},
          position: { x: 0, y: 0 },
        },
        {
          id: "5",
          type: "gvafpscounter",
          data: {
            "starting-frame": "500",
          },
          position: { x: 0, y: 0 },
        },
        {
          id: "6",
          type: "gvadetect",
          data: {
            model: "${YOLO11n_POST_MODEL}",
            device: "GPU",
            "pre-process-backend": "va-surface-sharing",
            "model-instance-id": "yolo11-pose",
          },
          position: { x: 0, y: 0 },
        },
        {
          id: "7",
          type: "queue2",
          data: {},
          position: { x: 0, y: 0 },
        },
        {
          id: "8",
          type: "gvatrack",
          data: {
            "tracking-type": "short-term-imageless",
          },
          position: { x: 0, y: 0 },
        },
        {
          id: "9",
          type: "gvawatermark",
          data: {},
          position: { x: 0, y: 0 },
        },
        {
          id: "10",
          type: "gvametaconvert",
          data: {
            format: "json",
            "json-indent": "4",
          },
          position: { x: 0, y: 0 },
        },
        {
          id: "11",
          type: "gvametapublish",
          data: {
            method: "file",
            "file-path": "/dev/null",
          },
          position: { x: 0, y: 0 },
        },
        {
          id: "12",
          type: "fakesink",
          data: {},
          position: { x: 0, y: 0 },
        },
      ];

      const rawEdges: ReactFlowEdge[] = [
        {
          id: "0",
          source: "0",
          target: "1",
        },
        {
          id: "1",
          source: "1",
          target: "2",
        },
        {
          id: "2",
          source: "2",
          target: "3",
        },
        {
          id: "3",
          source: "3",
          target: "4",
        },
        {
          id: "4",
          source: "4",
          target: "5",
        },
        {
          id: "5",
          source: "5",
          target: "6",
        },
        {
          id: "6",
          source: "6",
          target: "7",
        },
        {
          id: "7",
          source: "7",
          target: "8",
        },
        {
          id: "8",
          source: "8",
          target: "9",
        },
        {
          id: "9",
          source: "9",
          target: "10",
        },
        {
          id: "10",
          source: "10",
          target: "11",
        },
        {
          id: "11",
          source: "11",
          target: "12",
        },
      ];

      // Transform nodes to include custom types and properties
      const transformedNodes = transformApiNodes(rawNodes);

      // Apply Dagre layout to position nodes automatically
      const { nodes: layoutedNodes, edges: layoutedEdges } =
        getLayoutedElements(transformedNodes, rawEdges, "LR");

      setNodes(layoutedNodes);
      setEdges(layoutedEdges);
    }
  }, [pipelineData, setNodes, setEdges]);

  return (
    <div style={{ width: "100%", height: "100vh", position: "relative" }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        onPaneClick={onPaneClick}
        nodesDraggable={true}
        fitView
      >
        <Controls />
        <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
      </ReactFlow>

      <NodeDataPanel
        selectedNode={selectedNode}
        onNodeDataUpdate={handleNodeDataUpdate}
      />
    </div>
  );
};

export default PipelineEditor;
