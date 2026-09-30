import { HttpContextToken } from '@angular/common/http';

export const SHOULD_SKIP_ERROR_HANDLER = new HttpContextToken<boolean>(() => false);
