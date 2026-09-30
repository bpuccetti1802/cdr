/* eslint-disable @typescript-eslint/no-explicit-any */
import {
  Component,
  Input,
  Output,
  EventEmitter,
  ViewChild,
  OnChanges,
  SimpleChanges,
  signal,
  ChangeDetectionStrategy,
  OnDestroy,
  TemplateRef,
  effect,
  ViewEncapsulation,
} from '@angular/core';
import { CommonModule, NgIf } from '@angular/common';
import {
  PdfJsViewerModule,
  PdfJsViewerComponent,
  DocumentError,
  PagesInfo,
  ChangedScale,
  ChangedRotation,
  PresentationMode,
  FindMatchesCount,
  DocumentOutline,
  AnnotationLayerRenderEvent,
  BookmarkClick,
  GroupVisibilityConfig,
  ControlVisibilityConfig,
  AutoActionConfig,
  ErrorConfig,
  LayoutConfig,
} from 'ng2-pdfjs-viewer';
import { PdfViewerInput } from './view-models/pdf-viewer-input';
import { BaseHrefService } from '@mf/services/base-href/base-href.service';
import { SpinnerComponent } from '../spinner/spinner.component';
import { EventBus } from '@mf/core/event-bus/event-bus';
import { ToastTypes } from 'test-library-frankmd93';
import {
  AUTO_ACTIONS_OPTIONS,
  CONTROLS_OPTIONS,
  ERROR_HANDLING_OPTIONS,
  GROUP_VISIBILITY_OPTIONS,
  LAYOUT_CONFIG_OPTIONS,
} from './constants/config';
import { CursorType } from './constants/cursor-type';
import { ScrollType } from './constants/scroll-type';
import { SpreadType } from './constants/spread-type';
import { PageMode } from './constants/page-mode';
/**
 * PDF Viewer Component
 *
 * A wrapper component around ng2-pdfjs-viewer that provides a configurable PDF viewing experience
 * with sensible defaults, error handling, and event management.
 *
 * ## Usage
 *
 * This component is typically used with `app-dynamic-loader` for dynamic module loading:
 *
 * ```html
 * <app-dynamic-loader
 *   exposedModule="PdfViewerComponent"
 *   [inputsAndHandlers]="inputAndHandlersPdfViewerProps">
 * </app-dynamic-loader>
 * ```
 *
 * ```typescript
 * inputAndHandlersPdfViewerProps = {
 *   inputs: {
 *     pdfSrc: 'https://example.com/document.pdf',
 *     zoom: 'page-width',
 *     showDownload: true,
 *     showPrint: true,
 *     theme: 'light',
 *     locale: 'it-IT',
 *     errorHandling: {
 *       message: 'Errore nel caricamento del documento PDF. Riprovare.',
 *       override: true,
 *       append: true
 *     }
 *   },
 *   handlers: {
 *     documentLoad: () => console.log('PDF loaded'),
 *     documentError: (error) => console.error('PDF error:', error),
 *     pageChange: (page) => console.log('Page changed:', page)
 *   }
 * };
 * ```

 * ## Key Features
 * - Configurable via single `inputs` object (all properties optional)
 * - Automatic error handling with customizable messages
 * - Loading state management
 * - Comprehensive event system for PDF interactions
 * - Performance optimized with caching for complex configurations
 * - Supports URL, Blob, or Uint8Array PDF sources
 *
 * ## Configuration
 * All configuration is done through the `inputs` property. See `PdfViewerInput` interface
 * for available options including theming, toolbar controls, layout, and behavior settings.
 *
 * @example
 * ```typescript
 * // Basic usage with dynamic loader
 * inputAndHandlersPdfViewerProps = {
 *   inputs: {
 *     pdfSrc: '/assets/documents/sample.pdf',
 *     showDownload: true,
 *     locale: 'it-IT'
 *   }
 * };
 *
 * // Advanced usage with custom styling and error handling
 * inputAndHandlersPdfViewerProps = {
 *   inputs: {
 *     pdfSrc: blobObject,
 *     theme: 'dark',
 *     primaryColor: '#3498db',
 *     zoom: 'auto',
 *     showSidebar: true,
 *     pageMode: 'bookmarks',
 *     errorHandling: {
 *       message: 'Custom error message',
 *       override: true
 *     }
 *   },
 *   handlers: {
 *     documentLoad: this.handlePdfLoad.bind(this),
 *     pageChange: (page) => this.trackPageView(page)
 *   }
 * };
 * ```
 */
@Component({
  selector: 'app-pdf-viewer',
  standalone: true,
  imports: [CommonModule, PdfJsViewerModule, NgIf, SpinnerComponent],
  templateUrl: './pdf-viewer.component.html',
  styleUrl: './pdf-viewer.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  encapsulation: ViewEncapsulation.None,
})
export class PdfViewerComponent implements OnChanges, OnDestroy {
  /** Reference to the underlying PDF.js viewer component */
  @ViewChild('pdfViewer') pdfViewer!: PdfJsViewerComponent;

  /**
   * Configuration object for the PDF viewer.
   * All viewer settings (source, theme, controls, layout, etc.) are configured here.
   * See `PdfViewerInput` interface for all available options.
   *
   * When used with `app-dynamic-loader`, this is passed via `inputsAndHandlers.inputs`:
   * ```typescript
   * inputAndHandlersPdfViewerProps = {
   *   inputs: {
   *     pdfSrc: 'https://example.com/doc.pdf',
   *     zoom: 'page-width',
   *     showDownload: true,
   *     locale: 'it-IT'
   *   }
   * };
   * ```
   *
   * @example
   * ```typescript
   * // Direct usage
   * inputs: {
   *   pdfSrc: 'https://example.com/doc.pdf',
   *   zoom: 'page-width',
   *   showDownload: true
   * }
   * ```
   */
  @Input() inputs: Partial<PdfViewerInput> = {};

  /**
   * Base URL path for the shared library assets.
   * Automatically prepended to PDF source URLs and viewer folder paths.
   * Defaults to '/mfSharedLibrary' and is combined with baseHref service value.
   */
  @Input() baseUrl: string = '/mfSharedLibrary';

  /**
   * Emitted when the PDF document has finished loading successfully.
   * Use this to perform actions after the PDF is ready (e.g., navigate to specific page).
   */
  @Output() documentLoad = new EventEmitter();

  /**
   * Emitted when an error occurs while loading or rendering the PDF.
   * Contains error details including message and error type.
   */
  @Output() documentError = new EventEmitter<DocumentError>();

  /** Emitted when the user navigates to a different page. Provides the new page number (1-indexed). */
  @Output() pageChange = new EventEmitter<number>();

  /** Emitted when PDF pages are initialized. Provides total page count and page information. */
  @Output() pagesInit = new EventEmitter<PagesInfo>();

  /** Emitted when the zoom/scale level changes. Provides the new scale value. */
  @Output() scaleChange = new EventEmitter<ChangedScale>();

  /** Emitted when the document rotation changes. Provides the new rotation angle in degrees. */
  @Output() rotationChange = new EventEmitter<ChangedRotation>();

  /** Emitted when presentation/fullscreen mode is toggled. */
  @Output() presentationModeChanged = new EventEmitter<PresentationMode>();

  /** Emitted when the user clicks the "Open File" button. */
  @Output() openFile = new EventEmitter<void>();

  /** Emitted when the find/search functionality is used. */
  @Output() find = new EventEmitter<unknown>();

  /** Emitted when the find operation updates match count. */
  @Output() updateFindMatchesCount = new EventEmitter<FindMatchesCount>();

  /** Emitted when the document outline/bookmarks are loaded. */
  @Output() outlineLoaded = new EventEmitter<DocumentOutline>();

  /** Emitted when annotation layers are rendered. */
  @Output() annotationLayerRendered = new EventEmitter<AnnotationLayerRenderEvent>();

  /** Emitted when a bookmark in the outline is clicked. */
  @Output() bookmarkClick = new EventEmitter<BookmarkClick>();

  /** Emitted when the viewer becomes idle (no active operations). */
  @Output() idle = new EventEmitter<void>();

  /** Emitted after the print dialog is closed. */
  @Output() afterPrint = new EventEmitter<void>();

  /** Emitted when zoom level changes. Provides zoom value as string. */
  @Output() zoomChange = new EventEmitter<string>();

  /** Emitted when cursor type changes (HAND, SELECT, ZOOM). */
  @Output() cursorChange = new EventEmitter<string>();

  /** Emitted when scroll mode changes (VERTICAL, HORIZONTAL, WRAPPED). */
  @Output() scrollChange = new EventEmitter<string>();

  /** Emitted when spread mode changes (ODD, EVEN, NONE). */
  @Output() spreadChange = new EventEmitter<string>();

  /** Emitted when sidebar page mode changes (none, thumbs, bookmarks, attachments). */
  @Output() pageModeChange = new EventEmitter<string>();

  /** Signal indicating whether the PDF is currently loading. */
  isLoading = signal<boolean>(true);

  /** Signal indicating whether an error has occurred. */
  hasError = signal<boolean>(false);

  /** Signal containing the current error message, if any. */
  errorMessage = signal<string>('');

  // Cache for complex object getters to avoid recreating objects on every change detection
  private _controlVisibilityCache: ControlVisibilityConfig | null = null;
  private _autoActionsCache: AutoActionConfig | null = null;
  private _errorHandlingCache: ErrorConfig | null = null;
  private _groupVisibilityCache: GroupVisibilityConfig | null = null;
  private _layoutConfigCache: LayoutConfig | null = null;
  private _inputsVersion = 0;

  private readonly eventBus = EventBus.getInstance();

  constructor(private readonly baseHrefService: BaseHrefService) {
    this.baseUrl = this.baseHrefService.baseUrl + this.baseUrl;
    let previousErrorState = false;
    effect(() => {
      const hasError = this.hasError();
      const message = this.errorMessage();

      // Only show notification when error transitions from false to true
      if (hasError && !previousErrorState && message) {
        this.showErrorNotification();
      }

      previousErrorState = hasError;
    });
  }

  /**
   * @description This method shows an error notification when an error occurs while loading or rendering the PDF.
   * @returns void
   */
  private showErrorNotification(): void {
    this.eventBus.dispatchCustomEvent({
      eventName: 'notification-open-event',
      payload: {
        openNotification: true,
        toastType: ToastTypes.ERROR,
        titleContent: 'Errore nel caricamento del documento PDF',
        message: this.errorMessage() || 'Riprovare',
        useTimer: true,
      },
      reply: false,
    });
  }

  // ============================================================================
  // Configuration Getters
  // These getters provide default values for all viewer configuration options.
  // They read from the `inputs` object and return sensible defaults if not provided.
  // ============================================================================

  /** Unique identifier for the viewer instance. Default: 'pdf-viewer' */
  get viewerId(): string {
    return this.inputs?.viewerId ?? 'pdf-viewer';
  }

  get viewerFolder(): string {
    return this.baseUrl + (this.inputs?.viewerFolder ?? '/assets/pdfjs');
  }

  get externalWindow(): boolean {
    return this.inputs?.externalWindow ?? false;
  }

  get externalWindowOptions(): string {
    return this.inputs?.externalWindowOptions ?? '';
  }

  get target(): string {
    return this.inputs?.target ?? '_blank';
  }

  get theme(): 'light' | 'dark' | 'auto' {
    return this.inputs?.theme ?? 'light';
  }

  get primaryColor(): string | undefined {
    return this.inputs?.primaryColor;
  }

  get backgroundColor(): string | undefined {
    return this.inputs?.backgroundColor;
  }

  get pageBorderColor(): string | undefined {
    return this.inputs?.pageBorderColor;
  }

  get toolbarColor(): string | undefined {
    return this.inputs?.toolbarColor;
  }

  get textColor(): string | undefined {
    return this.inputs?.textColor;
  }

  /**
   * PDF document source (URL, Blob, or Uint8Array).
   * If a string URL is provided, it's automatically prefixed with baseUrl.
   * This is the primary required property for the viewer to function.
   */
  get pdfSource(): string | Blob | Uint8Array {
    if (this.inputs?.pdfBlobUint8Array) {
      return this.inputs?.pdfBlobUint8Array;
    }
    return this.baseUrl + (this.inputs?.pdfSrc ?? '');
  }

  get borderRadius(): string | undefined {
    return this.inputs?.borderRadius;
  }

  get customCSS(): string | undefined {
    return this.inputs?.customCSS;
  }

  get iframeTitle(): string {
    return this.inputs?.iframeTitle ?? 'PDF Viewer';
  }

  /* get customSpinnerTpl(): TemplateRef<any> | undefined {
    return this.inputs?.customSpinnerTpl;
  }
 */
  get spinnerClass(): string | undefined {
    return this.inputs?.spinnerClass;
  }

  get customErrorTpl(): TemplateRef<any> | undefined {
    return this.inputs?.customErrorTpl;
  }

  get errorClass(): string | undefined {
    return this.inputs?.errorClass;
  }

  get viewerPage(): number {
    return this.inputs?.page ?? 1;
  }

  get namedDest(): string {
    return this.inputs?.namedDest ?? '';
  }

  get rotation(): number {
    return this.inputs?.rotation ?? 0;
  }

  get downloadFileName(): string {
    return this.inputs?.downloadFileName ?? 'documento.pdf';
  }

  // ============================================================================
  // Memoized Configuration Getters
  // These getters cache complex configuration objects to improve performance
  // by avoiding object recreation on every change detection cycle.
  // Cache is invalidated when inputs change (see ngOnChanges).
  // ============================================================================

  /**
   * Fine-grained control visibility configuration.
   * Cached for performance. Controls which individual toolbar buttons are visible.
   */
  get controlVisibility(): ControlVisibilityConfig {
    if (!this._controlVisibilityCache) {
      this._controlVisibilityCache = {
        ...CONTROLS_OPTIONS,
        ...this.inputs?.controlVisibility,
      };
    }
    return this._controlVisibilityCache;
  }

  /**
   * Automatic actions configuration.
   * Cached for performance. Defines actions to perform automatically on PDF load.
   */
  get autoActions(): AutoActionConfig {
    if (!this._autoActionsCache) {
      this._autoActionsCache = {
        ...AUTO_ACTIONS_OPTIONS,
        ...this.inputs?.autoActions,
      };
    }
    return this._autoActionsCache;
  }

  /**
   * Error handling configuration.
   * Cached for performance. Customizes error messages and error display behavior.
   */
  get errorHandling(): ErrorConfig {
    if (!this._errorHandlingCache) {
      this._errorHandlingCache = {
        ...ERROR_HANDLING_OPTIONS,
        ...this.inputs?.errorHandling,
      };
    }
    return this._errorHandlingCache;
  }

  /**
   * Group visibility configuration.
   * Cached for performance. Controls visibility of toolbar and sidebar groups.
   */
  get groupVisibility(): GroupVisibilityConfig {
    if (!this._groupVisibilityCache) {
      this._groupVisibilityCache = {
        ...GROUP_VISIBILITY_OPTIONS,
        ...this.inputs?.groupVisibility,
      };
    }
    return this._groupVisibilityCache;
  }

  /**
   * Layout configuration.
   * Cached for performance. Defines toolbar position, sidebar width, and responsive breakpoints.
   */
  get layoutConfig(): LayoutConfig {
    if (!this._layoutConfigCache) {
      this._layoutConfigCache = {
        ...LAYOUT_CONFIG_OPTIONS,
        ...this.inputs?.layoutConfig,
      };
    }
    return this._layoutConfigCache;
  }

  get urlValidation(): boolean {
    return this.inputs?.urlValidation ?? false;
  }

  get iframeBorder(): string | number {
    return this.inputs?.iframeBorder || '0';
  }

  get viewerZoom(): string {
    const zoom = this.inputs?.zoom ?? 'page-width';
    return String(zoom);
  }

  get cursor(): CursorType {
    return this.inputs?.cursor ?? CursorType.SELECT;
  }

  get scroll(): ScrollType {
    return this.inputs?.scroll ?? ScrollType.VERTICAL;
  }

  get spread(): SpreadType {
    return this.inputs?.spread ?? SpreadType.NONE;
  }

  get pageMode(): PageMode {
    return this.inputs?.pageMode ?? PageMode.NONE;
  }

  get showSpinner(): boolean {
    return this.inputs?.showSpinner ?? false;
  }

  get locale(): string {
    return this.inputs?.locale ?? 'en-US';
  }

  get useOnlyCssZoom(): boolean {
    return this.inputs?.useOnlyCssZoom ?? false;
  }

  get diagnosticLogs(): boolean {
    return this.inputs?.diagnosticLogs ?? false;
  }

  /**
   * Handles input property changes.
   * Invalidates cached configuration objects when inputs change and resets error state
   * when PDF source changes to allow retry after errors.
   */
  ngOnChanges(changes: SimpleChanges): void {
    // Invalidate cache when inputs change
    if (changes['inputs']) {
      this._controlVisibilityCache = null;
      this._autoActionsCache = null;
      this._errorHandlingCache = null;
      this._groupVisibilityCache = null;
      this._layoutConfigCache = null;
      this._inputsVersion++;
    }
  }

  /**
   * Handles successful PDF document load.
   * Updates loading state and emits documentLoad event.
   */
  onDocumentLoadHandler(): void {
    this.isLoading.set(false);
    this.hasError.set(false);
    this.documentLoad?.emit();
  }

  /**
   * Handles PDF loading/rendering errors.
   * Updates error state with message from event or configured default, then emits documentError event.
   *
   * @param event - Error event containing error details from PDF.js
   */
  onDocumentErrorHandler(event: DocumentError): void {
    // Stop loading immediately and prevent further rendering attempts
    this.isLoading.set(false);
    this.hasError.set(true);

    // Use error message from event if available, otherwise use configured error message (Italian by default)
    const errorMessage =
      event?.message ||
      this.errorMessage() ||
      'Errore nel caricamento del documento PDF. Riprovare.';
    this.errorMessage.set(errorMessage);

    this.documentError?.emit(event);
  }

  onPageChangeHandler(pageNumber: number): void {
    this.pageChange?.emit(pageNumber);
  }

  onPagesInitHandler(event: PagesInfo): void {
    this.pagesInit?.emit(event);
  }

  onScaleChangeHandler(event: ChangedScale): void {
    this.scaleChange?.emit(event);
  }

  onRotationChangeHandler(event: ChangedRotation): void {
    this.rotationChange?.emit(event);
  }

  onPresentationModeChangedHandler(event: PresentationMode): void {
    this.presentationModeChanged?.emit(event);
  }

  onOpenFileHandler(): void {
    this.openFile?.emit();
  }

  onFindHandler(event: unknown): void {
    this.find?.emit(event);
  }

  onUpdateFindMatchesCountHandler(event: FindMatchesCount): void {
    this.updateFindMatchesCount?.emit(event);
  }

  onOutlineLoadedHandler(event: DocumentOutline): void {
    this.outlineLoaded?.emit(event);
  }

  onAnnotationLayerRenderedHandler(event: AnnotationLayerRenderEvent): void {
    this.annotationLayerRendered?.emit(event);
  }

  onBookmarkClickHandler(event: BookmarkClick): void {
    this.bookmarkClick?.emit(event);
  }

  onIdleHandler(): void {
    this.idle?.emit();
  }

  onAfterPrintHandler(): void {
    this.afterPrint?.emit();
  }

  onZoomChangeHandler(zoom: string): void {
    this.zoomChange?.emit(zoom);
  }

  onCursorChangeHandler(cursor: string): void {
    this.cursorChange?.emit(cursor);
  }

  onScrollChangeHandler(scroll: string): void {
    this.scrollChange?.emit(scroll);
  }

  onSpreadChangeHandler(spread: string): void {
    this.spreadChange?.emit(spread);
  }

  onPageModeChangeHandler(pageMode: string): void {
    this.pageModeChange?.emit(pageMode);
  }

  /**
   * Cleanup on component destruction.
   * Clears all cached objects, resets state signals, and properly closes the PDF viewer
   * to free resources and prevent memory leaks.
   */
  ngOnDestroy(): void {
    // Clear all cache objects to free memory
    this._controlVisibilityCache = null;
    this._autoActionsCache = null;
    this._errorHandlingCache = null;
    this._groupVisibilityCache = null;
    this._layoutConfigCache = null;

    this.isLoading.set(true);
    this.hasError.set(false);
    this.errorMessage.set('');

    // Close the PDF viewer if it exists (cleans up internal resources, event listeners, etc.)
    if (this.pdfViewer?.closeViewer) {
      try {
        this.pdfViewer.closeViewer();
      } catch (error) {
        console.error('Error closing PDF viewer:', error);
      }
    }
  }
}
