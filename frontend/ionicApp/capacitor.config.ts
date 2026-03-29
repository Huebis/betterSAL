import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'io.ionic.starter',
  appName: 'ionicApp',
  webDir: 'www',
  plugins:{
    SplashScreen:{
      launShowDuration:3000,
      launchAutoHide: true,
      backgroundColor: "#000000",
      androidScaleType: 'CENTER_CROP'

    }
  }
  /*plugins: {
    PushNotifications: {
      presentationOptions: [
        'badge', 'sound', 'alert'
      ]
    }
  }*/
};

export default config;
