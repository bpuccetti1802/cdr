import {
  Component,
  Input,
  OnInit,
  OnChanges,
  SimpleChanges,
  inject,
  ElementRef,
  NgZone,
  ViewChild,
  OnDestroy,
} from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { PLATFORM_ID } from '@angular/core';
import { LeafletModule } from '@bluehalo/ngx-leaflet';
import * as L from 'leaflet';
import { RadioComponent } from '../form-elements/radio/radio.component';
import { FormControl } from '@angular/forms';

export type RcWmsLayerConfig = {
  id: string;
  label: string;
  layerName: string;
  styles?: string;
};

export type RcMarker = {
  lat: number;
  lng: number;
  tooltip?: string;
  popup?: string;
  iconUrl?: string;
  iconSize?: [number, number];
  iconAnchor?: [number, number];
  popupAnchor?: [number, number];
  data?: unknown;
};

@Component({
  selector: 'app-map',
  standalone: true,
  imports: [CommonModule, LeafletModule, RadioComponent],
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss'],
})
export class MapComponent implements OnInit, OnChanges, OnDestroy {
  /** —— Config base —— */
  @Input() center: L.LatLngExpression = [41.9028, 12.4964];
  @Input() zoom = 12;
  @Input() minZoom = 1;
  @Input() maxZoom = 20;

  /** —— Tile layer —— */
  @Input() tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
  @Input() tileOptions: Partial<L.TileLayerOptions> = {
    attribution: '&copy; OpenStreetMap contributors',
    crossOrigin: true,
  };

  /** —— Interazione —— */
  @Input() dragging = true;
  @Input() scrollWheelZoom = true;
  @Input() doubleClickZoom = true;
  @Input() touchZoom = true;
  @Input() zoomControl = true;

  /** —— Presentazione contenitore —— */
  @Input() height = '400px';
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  @Input() containerClass: string | string[] | Set<string> | { [klass: string]: any } = '';

  /** —— Markers & fit —— */
  @Input() markers: RcMarker[] = [];
  @Input() fitBounds?: L.LatLngBoundsExpression;
  @Input() fitToMarkers = true;
  @Input() autoFitOnMarkersChange = true;
  @Input() fitBoundsPadding: [number, number] = [20, 20];

  /** —— Asset icone —— */
  @Input() leafletAssetsBaseUrl = '/assets/leaflet/';

  /** —— Callback —— */
  @Input() onMapReady?: (map: L.Map) => void;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  @Input() onMapClick?: (event: any) => void;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  @Input() onMoveEnd?: (event: any) => void;

  @Input() showLayerControls = true;
  @Input() availableLayers: RcWmsLayerConfig[] = [];
  @Input() onLayerChange?: (activeLayerId: string | null) => void;

  @ViewChild('host', { static: true }) host!: ElementRef<HTMLDivElement>;

  private zone = inject(NgZone);
  private map?: L.Map;
  private markersRefs: L.Marker[] = [];
  private platformId = inject(PLATFORM_ID);
  private ro?: ResizeObserver;
  private firstVisibleDone = false;
  isBrowser = isPlatformBrowser(this.platformId);
  leafletOptions!: L.MapOptions;
  layersPanelOpen = false;
  activeLayerId: string | null = null;

  /** —— Radio button  —— */
  NONE = '__none__';
  selectedLayerCtrl = new FormControl<string>(this.NONE);

  get layerRadioItems() {
    return this.availableLayers.map((l) => ({ value: l.id, label: l.label }));
  }

  ngOnInit(): void {
    if (!this.isBrowser) return;
    this.patchDefaultMarkerIcons();
    this.leafletOptions = {
      center: this.center,
      zoom: this.zoom,
      minZoom: this.minZoom,
      maxZoom: this.maxZoom,
      zoomControl: this.zoomControl,
      dragging: this.dragging,
      scrollWheelZoom: this.scrollWheelZoom,
      doubleClickZoom: this.doubleClickZoom,
      touchZoom: this.touchZoom,
      layers: [L.tileLayer(this.tileUrl, { ...this.tileOptions, maxNativeZoom: 19, maxZoom: 19 })],
    };
    this.zone.runOutsideAngular(() => {
      try {
        this.ro = new ResizeObserver(() => this.map?.invalidateSize());
        this.ro.observe(this.host.nativeElement);
      } catch {
        setTimeout(() => this.map?.invalidateSize(), 120);
      }
    });

    this.selectedLayerCtrl.valueChanges.subscribe((id) => {
      const next = id === this.NONE ? null : id!;
      this.activeLayerId = next;
      this.onLayerChange?.(next);
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (!this.isBrowser || !this.map) return;

    if (changes['markers']) {
      this.clearMarkers();
      this.renderMarkers();
      if (this.autoFitOnMarkersChange) this.applyInitialFit();
    }
  }

  // Event handlers
  handleMapReady(m: L.Map) {
    this.map = m;
    setTimeout(() => m.invalidateSize(), 0);
    this.renderMarkers();
    this.onMapReady?.(m);
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  handleClick(event: any) {
    this.onMapClick?.(event);
  }
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  handleMoveEnd(event: any) {
    console.log('[Modal] move/zoom end', event);
    this.onMoveEnd?.(event);
  }
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  handleZoomEnd(event: any) {
    this.onMoveEnd?.(event);
  }

  // Helpers
  private renderMarkers(): void {
    if (!this.map || !this.markers?.length) return;
    this.markers.forEach((m) => {
      const mIcon = m.iconUrl
        ? L.icon({
            iconUrl: m.iconUrl,
            iconSize: m.iconSize ?? [25, 41],
            iconAnchor: m.iconAnchor ?? [12, 41],
            popupAnchor: m.popupAnchor ?? [1, -34],
            shadowUrl: this.leafletAssetsBaseUrl + 'marker-shadow.png',
          })
        : undefined;

      const mk = L.marker([m.lat, m.lng], mIcon ? { icon: mIcon } : undefined).addTo(this.map!);
      if (m.tooltip) mk.bindTooltip(m.tooltip);
      if (m.popup) mk.bindPopup(m.popup);
      this.markersRefs.push(mk);
    });
  }

  private clearMarkers(): void {
    if (!this.map) return;
    this.markersRefs.forEach((mk) => this.map!.removeLayer(mk));
    this.markersRefs = [];
  }

  private applyInitialFit(): void {
    if (!this.map) return;

    if (this.fitBounds) {
      this.map.fitBounds(this.fitBounds, { padding: this.fitBoundsPadding });
      return;
    }
    if (this.fitToMarkers && this.markers?.length) {
      const bounds = L.latLngBounds(this.markers.map((m) => L.latLng(m.lat, m.lng)));
      this.map.fitBounds(bounds, { padding: this.fitBoundsPadding });
    }
  }

  private patchDefaultMarkerIcons(): void {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (L.Icon.Default as any).mergeOptions({
      iconRetinaUrl: this.leafletAssetsBaseUrl + 'marker-icon-2x.png',
      iconUrl: this.leafletAssetsBaseUrl + 'marker-icon.png',
      shadowUrl: this.leafletAssetsBaseUrl + 'marker-shadow.png',
    });
  }

  toggleLayersPanel() {
    this.layersPanelOpen = !this.layersPanelOpen;
    this.map?.invalidateSize();
  }

  syncNoneIfNeeded() {
    if (this.selectedLayerCtrl.value !== this.NONE) {
      this.selectedLayerCtrl.setValue(this.NONE, { emitEvent: false });
    }
  }

  syncNoneAndEmitClear() {
    if (this.selectedLayerCtrl.value !== this.NONE) {
      this.selectedLayerCtrl.setValue(this.NONE, { emitEvent: false });
    }
    this.activeLayerId = null;
    this.onLayerChange?.(null);
  }

  ngOnDestroy(): void {
    this.ro?.disconnect();
  }
}
