export type CargoRequest = {
  commodity: string;
  quantityMt: number;
  originCountry: string;
  originPort: string;
  destinationPort: string;
  requiredDeliveryDate: string;
  numberOfVoyages: number;
  contractDuration: string;
  vesselType: string;
};

export type Vessel = {
  vesselId: string;
  vesselName: string;
  vesselType: string;
  dwt: number;
  loaM: number;
  beamM: number;
  draftM: number;
  availableFrom: string;
  estimatedSpeed: number;
  fuelConsumption: number;
};

export type Port = {
  portId: string;
  portName: string;
  maxDraftM: number;
  maxLoaM: number;
  maxBeamM: number;
  cargoHandlingRateTpd: number;
  avgWaitingHours: number;
  congestion: string;
  berthingStatus: string;
};

export type FreightForecast = {
  currentRate: number;
  forecast7d: number;
  forecast15d: number;
  forecast30d: number;
  forecast60d: number;
  forecast90d: number;
  lowerBound: number;
  upperBound: number;
  trend: string;
  confidence: number;
  modelVersion: string;
};

export type ContractScenario = {
  contractType: string;
  numberOfVoyages: number;
  durationMonths: number;
  estimatedFreightCost: number;
  idleCost: number;
  deadheadCost: number;
  totalEstimatedCost: number;
  riskScore: number;
  flexibilityScore: number;
};

export const defaultCargo: CargoRequest = {
  commodity: 'Coal',
  quantityMt: 75000,
  originCountry: 'Australia',
  originPort: 'Newcastle',
  destinationPort: 'Paradip',
  requiredDeliveryDate: '2025-10-28',
  numberOfVoyages: 4,
  contractDuration: 'Short Term',
  vesselType: 'Capesize',
};

export const vessels: Vessel[] = [
  { vesselId: 'V-1042', vesselName: 'Pacific Meridian', vesselType: 'Capesize', dwt: 181000, loaM: 292, beamM: 45, draftM: 18.1, availableFrom: '2025-09-18', estimatedSpeed: 13.8, fuelConsumption: 48 },
  { vesselId: 'V-2219', vesselName: 'Atlas Horizon', vesselType: 'Capesize', dwt: 176500, loaM: 289, beamM: 45, draftM: 17.7, availableFrom: '2025-09-27', estimatedSpeed: 13.4, fuelConsumption: 46 },
  { vesselId: 'V-3371', vesselName: 'Cobalt Trader', vesselType: 'Newcastlemax', dwt: 208000, loaM: 300, beamM: 47, draftM: 19.2, availableFrom: '2025-10-02', estimatedSpeed: 13.1, fuelConsumption: 53 },
  { vesselId: 'V-5920', vesselName: 'Silver Tern', vesselType: 'Panamax', dwt: 82_500, loaM: 229, beamM: 32, draftM: 14.2, availableFrom: '2025-09-14', estimatedSpeed: 13.6, fuelConsumption: 29 },
  { vesselId: 'V-7018', vesselName: 'Boreal Crest', vesselType: 'Capesize', dwt: 169000, loaM: 284, beamM: 44, draftM: 17.3, availableFrom: '2025-10-11', estimatedSpeed: 14.2, fuelConsumption: 45 },
];

export const ports: Port[] = [
  { portId: 'P-NEC', portName: 'Newcastle, AU', maxDraftM: 17.8, maxLoaM: 300, maxBeamM: 47, cargoHandlingRateTpd: 68000, avgWaitingHours: 31, congestion: 'Moderate', berthingStatus: 'Operating' },
  { portId: 'P-PAR', portName: 'Paradip, IN', maxDraftM: 17.2, maxLoaM: 285, maxBeamM: 45, cargoHandlingRateTpd: 54000, avgWaitingHours: 54, congestion: 'Elevated', berthingStatus: 'Tide restricted' },
  { portId: 'P-RIC', portName: 'Richards Bay, ZA', maxDraftM: 17.5, maxLoaM: 290, maxBeamM: 45, cargoHandlingRateTpd: 61000, avgWaitingHours: 42, congestion: 'Moderate', berthingStatus: 'Operating' },
  { portId: 'P-HAM', portName: 'Hampton Roads, US', maxDraftM: 15.5, maxLoaM: 280, maxBeamM: 43, cargoHandlingRateTpd: 49000, avgWaitingHours: 22, congestion: 'Low', berthingStatus: 'Operating' },
  { portId: 'P-BAL', portName: 'Baltimore, US', maxDraftM: 14.7, maxLoaM: 260, maxBeamM: 40, cargoHandlingRateTpd: 33000, avgWaitingHours: 18, congestion: 'Low', berthingStatus: 'Operating' },
];

export const forecast: FreightForecast = {
  currentRate: 23.85, forecast7d: 24.7, forecast15d: 25.4, forecast30d: 26.9, forecast60d: 24.8, forecast90d: 23.5,
  lowerBound: 21.2, upperBound: 28.7, trend: 'Firming near term', confidence: 78, modelVersion: 'FIQ-Capesize v4.6',
};

export const scenarios: ContractScenario[] = [
  { contractType: 'Spot', numberOfVoyages: 1, durationMonths: 1, estimatedFreightCost: 1_788_750, idleCost: 0, deadheadCost: 82_400, totalEstimatedCost: 1_871_150, riskScore: 68, flexibilityScore: 94 },
  { contractType: 'Short-term MVC', numberOfVoyages: 4, durationMonths: 3, estimatedFreightCost: 6_984_000, idleCost: 128_600, deadheadCost: 148_000, totalEstimatedCost: 7_260_600, riskScore: 37, flexibilityScore: 72 },
  { contractType: 'Medium-term MVC', numberOfVoyages: 8, durationMonths: 6, estimatedFreightCost: 13_841_600, idleCost: 244_000, deadheadCost: 191_000, totalEstimatedCost: 14_276_600, riskScore: 29, flexibilityScore: 49 },
];

export const marketSeries = [
  { date: '04 Aug', actual: 21.8, forecast: null, low: null, high: null },
  { date: '11 Aug', actual: 22.4, forecast: null, low: null, high: null },
  { date: '18 Aug', actual: 22.1, forecast: null, low: null, high: null },
  { date: '25 Aug', actual: 23.0, forecast: null, low: null, high: null },
  { date: '01 Sep', actual: 23.5, forecast: 23.5, low: 22.8, high: 24.2 },
  { date: '08 Sep', actual: 23.9, forecast: 23.9, low: 22.9, high: 25.0 },
  { date: '15 Sep', actual: null, forecast: 24.7, low: 23.2, high: 26.2 },
  { date: '22 Sep', actual: null, forecast: 25.4, low: 23.5, high: 27.1 },
  { date: '29 Sep', actual: null, forecast: 26.9, low: 24.1, high: 28.7 },
  { date: '06 Oct', actual: null, forecast: 26.2, low: 22.9, high: 29.5 },
  { date: '13 Oct', actual: null, forecast: 24.8, low: 21.9, high: 27.7 },
  { date: '27 Oct', actual: null, forecast: 23.5, low: 21.2, high: 25.8 },
];

export const routeRows = [
  { route: 'Newcastle → Paradip', commodity: 'Thermal coal', rate: 23.85, change: '+4.2%', status: 'Firming', eta: '12–16 days' },
  { route: 'Richards Bay → Rotterdam', commodity: 'Thermal coal', rate: 22.6, change: '+2.8%', status: 'Stable', eta: '20–24 days' },
  { route: 'Tubarao → Qingdao', commodity: 'Iron ore', rate: 28.2, change: '-1.1%', status: 'Softening', eta: '35–38 days' },
  { route: 'Hampton Roads → Rotterdam', commodity: 'Grain', rate: 19.4, change: '+0.7%', status: 'Stable', eta: '15–18 days' },
];

export const alerts = [
  { title: 'Paradip tide window compressed', detail: 'Berthing queue +18h vs 7-day average', severity: 'High', time: '18 min ago' },
  { title: 'Capesize availability tightening', detail: '12 suitable open tonnage signals in basin', severity: 'Watch', time: '46 min ago' },
  { title: 'Fuel spread widened', detail: 'Singapore VLSFO +$11.20/mt week on week', severity: 'Medium', time: '2h ago' },
];