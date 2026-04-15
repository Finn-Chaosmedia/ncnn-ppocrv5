// Tencent is pleased to support the open source community by making ncnn available.
//
// Copyright (C) 2025 THL A29 Limited, a Tencent company. All rights reserved.
//
// Licensed under the BSD 3-Clause License (the "License"); you may not use this file except
// in compliance with the License. You may obtain a copy of the License at
//
// https://opensource.org/licenses/BSD-3-Clause
//
// Unless required by applicable law or agreed to in writing, software distributed
// under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
// CONDITIONS OF ANY KIND, either express or implied. See the License for the
// specific language governing permissions and limitations under the License.

package com.tencent.ppocrv5ncnn;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.graphics.PixelFormat;
import android.os.Bundle;
import android.util.Log;
import android.view.Surface;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.view.WindowManager;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.Spinner;

import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.widget.Toast;
import android.content.ClipboardManager;
import android.content.ClipData;
import android.content.Context;
import android.widget.EditText;
import android.widget.LinearLayout;

public class MainActivity extends Activity implements SurfaceHolder.Callback
{
    public static final int REQUEST_CAMERA = 100;

    private PPOCRv5Ncnn ppocrv5ncnn = new PPOCRv5Ncnn();
    private int facing = 0;

    private Spinner spinnerModel;
    private Spinner spinnerSize;
    private Spinner spinnerCPUGPU;
    private int current_model = 0;
    private int current_size = 0;
    private int current_cpugpu = 0;

    private SurfaceView cameraView;
    private Button buttonCapture;
    private LinearLayout resultContainer;
    private EditText textResult;
    private Button buttonCopy;
    private Button buttonReset;

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        cameraView = (SurfaceView) findViewById(R.id.cameraview);

        cameraView.getHolder().setFormat(PixelFormat.RGBA_8888);
        cameraView.getHolder().addCallback(this);

        Button buttonSwitchCamera = (Button) findViewById(R.id.buttonSwitchCamera);
        buttonSwitchCamera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View arg0) {

                int new_facing = 1 - facing;

                ppocrv5ncnn.closeCamera();

                ppocrv5ncnn.openCamera(new_facing);

                facing = new_facing;
            }
        });

        buttonCapture = (Button) findViewById(R.id.buttonCapture);
        buttonCapture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d("OCR", "Foto-Button geklickt - OCR gestartet");
                
                // Echte OCR aufrufen
                String ocrResult = ppocrv5ncnn.captureAndOCR();
                
                // Log Ergebnis
                Log.d("OCR Result", "Erkannt: " + ocrResult);
                
                // Ergebnis anzeigen
                if (ocrResult == null || ocrResult.isEmpty()) {
                    ocrResult = "Kein Text erkannt. Bitte Kamera auf Text richten.";
                }
                
                textResult.setText(ocrResult);
                resultContainer.setVisibility(View.VISIBLE);
                
                // Toast für Benutzerfeedback
                Toast.makeText(MainActivity.this, 
                    "OCR abgeschlossen", Toast.LENGTH_SHORT).show();
            }
        });

        // Copy-Button und Reset-Button initialisieren
        resultContainer = (LinearLayout) findViewById(R.id.resultContainer);
        textResult = (EditText) findViewById(R.id.textResult);
        buttonCopy = (Button) findViewById(R.id.buttonCopy);
        buttonReset = (Button) findViewById(R.id.buttonReset);
        
        buttonCopy.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Text in Zwischenablage kopieren
                ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
                ClipData clip = ClipData.newPlainText("OCR Result", textResult.getText().toString());
                clipboard.setPrimaryClip(clip);
                
                Toast.makeText(MainActivity.this, 
                    "Text in Zwischenablage kopiert!", Toast.LENGTH_SHORT).show();
            }
        });
        
        // Reset-Button: Versteckt das Ergebnis und ermöglicht neue Aufnahme
        buttonReset.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Textfeld leeren
                textResult.setText("");
                
                // Ergebnis-Container ausblenden
                resultContainer.setVisibility(View.GONE);
                
                // Toast für Benutzerfeedback
                Toast.makeText(MainActivity.this, 
                    "Bereit für neue Aufnahme", Toast.LENGTH_SHORT).show();
                
                Log.d("OCR", "Reset-Button: Bereit für neue OCR");
            }
        });

        spinnerModel = (Spinner) findViewById(R.id.spinnerModel);
        spinnerModel.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> arg0, View arg1, int position, long id)
            {
                if (position != current_model)
                {
                    current_model = position;
                    reload();
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> arg0)
            {
            }
        });

        spinnerSize = (Spinner) findViewById(R.id.spinnerSize);
        spinnerSize.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> arg0, View arg1, int position, long id)
            {
                if (position != current_size)
                {
                    current_size = position;
                    reload();
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> arg0)
            {
            }
        });

        spinnerCPUGPU = (Spinner) findViewById(R.id.spinnerCPUGPU);
        spinnerCPUGPU.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> arg0, View arg1, int position, long id)
            {
                if (position != current_cpugpu)
                {
                    current_cpugpu = position;
                    reload();
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> arg0)
            {
            }
        });

        reload();
    }

    private void reload()
    {
        boolean ret_init = ppocrv5ncnn.loadModel(getAssets(), current_model, current_size, current_cpugpu);
        if (!ret_init)
        {
            Log.e("MainActivity", "ppocrv5ncnn loadModel failed");
        }
    }

    @Override
    public void surfaceChanged(SurfaceHolder holder, int format, int width, int height)
    {
        ppocrv5ncnn.setOutputWindow(holder.getSurface());
    }

    @Override
    public void surfaceCreated(SurfaceHolder holder)
    {
    }

    @Override
    public void surfaceDestroyed(SurfaceHolder holder)
    {
    }

    @Override
    public void onResume()
    {
        super.onResume();

        if (ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.CAMERA) == PackageManager.PERMISSION_DENIED)
        {
            ActivityCompat.requestPermissions(this, new String[] {Manifest.permission.CAMERA}, REQUEST_CAMERA);
        }

        ppocrv5ncnn.openCamera(facing);
    }

    @Override
    public void onPause()
    {
        super.onPause();

        ppocrv5ncnn.closeCamera();
    }
}
