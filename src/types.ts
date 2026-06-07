/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export interface ChannelAllocation {
  metaPercent: number;
  googlePercent: number;
  programmaticPercent: number;
  creativeCROPercent: number;
}

export interface CreativeHook {
  angle: string;
  hookText: string;
  visualConcept: string;
  targetChannel: string;
}

export interface TargetPersona {
  audiencename: string;
  demographicsDetailed: string;
  triggerPoints: string;
  funnelPosition: string; // TOF, MOF, BOF
}

export interface ProjectedMetrics {
  ctrLowBound: number;
  ctrHighBound: number;
  cpaImprovementPct: number;
  roasMultiplier: number;
}

export interface AdAuditStrategy {
  executiveSummary: string;
  channelAllocation: ChannelAllocation;
  creativeHooks: CreativeHook[];
  targetPersonas: TargetPersona[];
  actionPlanSteps: string[];
  projectedMetrics: ProjectedMetrics;
}

export interface CaseStudy {
  id: string;
  clientName: string;
  industry: string;
  heroHeadline: string;
  description: string;
  beforeCPA: number;
  afterCPA: number;
  beforeROAS: number;
  afterROAS: number;
  liftPercentage: number;
  revenueGenerated: string;
  imageSeedPrompt: string;
  approachSteps: string[];
  campaignType: string;
  bannerImage: string;
}

export interface SimulatorStats {
  adSpend: number;
  conversionRate: number;
  avgOrderValue: number;
  ctr: number;
}
