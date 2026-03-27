import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { TeacherAbsencesSubpage } from './teacher-absences.subpage';

describe('TeacherAbsencesComponent', () => {
  let component: TeacherAbsencesSubpage;
  let fixture: ComponentFixture<TeacherAbsencesSubpage>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ TeacherAbsencesSubpage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(TeacherAbsencesSubpage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
