import { HttpContextToken } from '@angular/common/http';

export const SHOULD_SKIP_LOADING_HANDLER = new HttpContextToken<boolean>(() => false);
