//Gard um zu entscheiden wer die seite sehen darf/soll (Lehrer und schüler manchmal unterschiedlich)


import { Injectable } from '@angular/core';
import { CanMatch, Route, UrlSegment } from '@angular/router';
import { AuthService } from './auth';

@Injectable({ providedIn: 'root' })
export class CanMatchGuard implements CanMatch {

  constructor(private authService: AuthService) {}

  canMatch(
    route: Route,
    segments: UrlSegment[]
  ): boolean {

    const allowedRoles: boolean[] = route.data?.['allowedRoles'] ?? [];

    return allowedRoles[this.authService.getRole()];

  }
}
