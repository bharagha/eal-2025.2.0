import { useParams } from "react-router";
import {
  useGetPipelineQuery,
  useRunPipelineMutation,
  useStopPipelineInstanceMutation,
} from "@/api/api.generated";
import {
  Background,
  BackgroundVariant,
  Controls,
  type Edge,
  type Node,
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
import FpsDisplay from "@/features/pipeline-editor/FpsDisplay.tsx";
import { toast } from "sonner";
import RunPipelineButton from "@/features/pipeline-editor/RunPipelineButton.tsx";
import StopPipelineButton from "@/features/pipeline-editor/StopPipelineButton.tsx";
import StatePreviewButton from "@/features/pipeline-editor/StatePreviewButton.tsx";

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

const nodeHeight = 120;

// Function to get node width based on node type
const getNodeWidth = (nodeType: string): number => {
  return nodeWidths[nodeType] || defaultNodeWidth;
};

const transformApiNodes = (apiNodes: Node[]): Node[] => {
  return apiNodes.map((node) => {
    return {
      ...node,
      type: node.type,
    };
  });
};

const getLayoutedElements = (
  nodes: Node[],
  edges: Edge[],
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

type UrlParams = {
  id: string;
};

const Pipelines = () => {
  const { id } = useParams<UrlParams>();
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [pipelineInstanceId, setPipelineInstanceId] = useState<string | null>(
    null,
  );

  const { data, isSuccess } = useGetPipelineQuery(
    {
      name: "predefined_pipelines",
      version: id!,
    },
    {
      skip: !id,
    },
  );

  const [runPipeline, { isLoading: isRunning }] = useRunPipelineMutation();
  const [stopPipelineInstance, { isLoading: isStopping }] =
    useStopPipelineInstanceMutation();

  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);

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
    setNodes((currentNodes) =>
      currentNodes.map((node) =>
        node.id === nodeId ? { ...node, data: updatedData } : node,
      ),
    );
  };

  // Handle pipeline execution
  const handleRunPipeline = async () => {
    if (!id) return;

    try {
      // Convert ReactFlow nodes to API format
      const apiNodes = nodes.map((node) => ({
        id: node.id,
        type: node.type || "default",
        data: Object.fromEntries(
          Object.entries(node.data || {}).map(([key, value]) => [
            key,
            String(value),
          ]),
        ),
      }));

      const response = await runPipeline({
        name: "predefined_pipelines",
        version: id,
        pipelineRequestRunInput: {
          async_: true,
          source: {
            type: "uri",
            uri: "https://storage.openvinotoolkit.org/repositories/openvino_notebooks/data/data/video/people.mp4",
          },
          parameters: {
            inferencing_channels: 20,
            recording_channels: 0,
            launch_config: {
              nodes: apiNodes,
              edges,
            },
          },
          tags: {
            additionalProp1: "string",
          },
        },
      }).unwrap();

      // Store the instance ID from the response
      if (
        response &&
        typeof response === "object" &&
        "instance_id" in response
      ) {
        setPipelineInstanceId(response.instance_id as string);
      }

      // Handle success (could show a toast notification)
      toast.success("Pipeline run started", {
        description: new Date().toISOString(),
      });
      console.log("Pipeline started successfully");
    } catch (error) {
      // Handle error (could show an error toast)
      toast.error("Failed to start pipeline", {
        description: error instanceof Error ? error.message : "Unknown error",
      });
      console.error("Failed to start pipeline:", error);
    }
  };

  // Handle pipeline stop
  const handleStopPipeline = async () => {
    if (!pipelineInstanceId) return;

    try {
      await stopPipelineInstance({
        instanceId: pipelineInstanceId,
      }).unwrap();

      // Clear the instance ID
      setPipelineInstanceId(null);

      // Handle success
      toast.success("Pipeline stopped", {
        description: new Date().toISOString(),
      });
      console.log("Pipeline stopped successfully");
    } catch (error) {
      // Handle error
      toast.error("Failed to stop pipeline", {
        description: error instanceof Error ? error.message : "Unknown error",
      });
      console.error("Failed to stop pipeline:", error);
    }
  };

  useEffect(() => {
    if (isSuccess && data?.launch_config) {
      // Get the raw nodes and edges from API
      // const rawNodes = data.launch_config.nodes || [];
      // const rawEdges = data.launch_config.edges || [];

      const rawNodes = [
        {
          id: "0",
          type: "filesrc",
          data: {
            location: "${VIDEO}",
          },
        },
        {
          id: "1",
          type: "qtdemux",
          data: {},
        },
        {
          id: "2",
          type: "h264parse",
          data: {},
        },
        {
          id: "3",
          type: "vah264dec",
          data: {},
        },
        {
          id: "4",
          type: "video/x-raw(memory:VAMemory)",
          data: {},
        },
        {
          id: "5",
          type: "gvafpscounter",
          data: {
            "starting-frame": "500",
          },
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
        },
        {
          id: "7",
          type: "queue2",
          data: {},
        },
        {
          id: "8",
          type: "gvatrack",
          data: {
            "tracking-type": "short-term-imageless",
          },
        },
        {
          id: "9",
          type: "gvawatermark",
          data: {},
        },
        {
          id: "10",
          type: "gvametaconvert",
          data: {
            format: "json",
            "json-indent": "4",
          },
        },
        {
          id: "11",
          type: "gvametapublish",
          data: {
            method: "file",
            "file-path": "/dev/null",
          },
        },
        {
          id: "12",
          type: "fakesink",
          data: {},
        },
      ];

      const rawEdges = [
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
      const transformedNodes = transformApiNodes(rawNodes as Node[]);

      // Apply Dagre layout to position nodes automatically
      const { nodes: layoutedNodes, edges: layoutedEdges } =
        getLayoutedElements(transformedNodes, rawEdges, "LR");

      setNodes(layoutedNodes);
      setEdges(layoutedEdges);
    }
  }, [isSuccess, data, setNodes, setEdges]);

  if (isSuccess) {
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

        <div className="absolute top-4 right-4 z-10 flex flex-col gap-2 items-end">
          {/* FPS Display */}
          <FpsDisplay />

          <div className="flex gap-2">
            {pipelineInstanceId ? (
              <StopPipelineButton
                isStopping={isStopping}
                onStopPipeline={handleStopPipeline}
              />
            ) : (
              <RunPipelineButton
                isRunning={isRunning}
                onRunPipeline={handleRunPipeline}
              />
            )}

            <StatePreviewButton edges={edges} nodes={nodes} />
          </div>
        </div>

        <NodeDataPanel
          selectedNode={selectedNode}
          onNodeDataUpdate={handleNodeDataUpdate}
        />
      </div>
    );
  }

  return <div>Loading pipeline: {id}</div>;
};

export default Pipelines;
