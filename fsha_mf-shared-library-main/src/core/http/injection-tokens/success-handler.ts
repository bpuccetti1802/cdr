import { HttpContextToken } from '@angular/common/http';

export const SHOULD_SKIP_SUCCESS_HANDLER = new HttpContextToken<boolean>(() => true);
