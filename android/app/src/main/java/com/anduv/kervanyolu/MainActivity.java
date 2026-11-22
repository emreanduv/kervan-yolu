package com.anduv.kervanyolu;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    // Ekran uyanık kalsın: oyun/uygulama açıkken dokunulmasa da kararmasın (sürüş sırasında)
    @Override
    public void onCreate(android.os.Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().addFlags(android.view.WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
    }
    // SES KORUYUCU (Mr. Anduv! standardı, 22 Kas 2026): uygulamaya dönünce web sesini uyandır
    @Override
    public void onResume() {
        super.onResume();
        try {
            if (getBridge() != null && getBridge().getWebView() != null) {
                getBridge().getWebView().onResume();
                getBridge().getWebView().postDelayed(() -> getBridge().getWebView().evaluateJavascript("window.sesKurtar&&window.sesKurtar()", null), 250);
            }
        } catch (Exception e) { }
    }
}
