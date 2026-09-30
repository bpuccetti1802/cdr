import {
  AutoActionConfig,
  ControlVisibilityConfig,
  ErrorConfig,
  GroupVisibilityConfig,
  LayoutConfig,
} from 'ng2-pdfjs-viewer';

export const CONTROLS_OPTIONS = {
  openFile: false,
  download: true,
  print: true,
  fullScreen: true,
  find: true,
  viewBookmark: false,
  annotations: false,
} satisfies ControlVisibilityConfig;

export const AUTO_ACTIONS_OPTIONS = {
  downloadOnLoad: false,
  printOnLoad: false,
  showLastPageOnLoad: false,
  rotateCW: false,
  rotateCCW: false,
} satisfies AutoActionConfig;

export const ERROR_HANDLING_OPTIONS = {
  message: 'Errore nel caricamento del documento PDF. Riprovare.',
  override: false,
  append: false,
} satisfies ErrorConfig;

export const GROUP_VISIBILITY_OPTIONS = {
  toolbarLeft: true,
  toolbarMiddle: true,
  toolbarRight: true,
  secondaryToolbarToggle: true,
  sidebar: true,
  sidebarLeft: true,
  sidebarRight: false,
} satisfies GroupVisibilityConfig;

export const LAYOUT_CONFIG_OPTIONS = {
  toolbarDensity: 'default',
  sidebarWidth: '250px',
  toolbarPosition: 'top',
  sidebarPosition: 'left',
  responsiveBreakpoint: '768px',
} satisfies LayoutConfig;
