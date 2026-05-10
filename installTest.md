# OMI-Tasks-Supabase Installer Test

- Test started: 2026-05-10T22:05:29+00:00
- Test VM: omi-tasks-install-test / 10.100.101.158 172.17.0.1
- Test user: gtgb
- OS: Ubuntu 26.04 LTS
- Scope: private GitHub repo clone, installer install with local Postgres and n8n, schema/UI checks, task candidate approval/edit/trash/restore/scratch flows, full uninstall, cleanup verification.
- Secrets: generated UI credentials and GitHub token used for private clone were not recorded or persisted.


## 1. Baseline VM and prerequisites

`uname -a`
Linux omi-tasks-install-test 7.0.0-14-generic #14-Ubuntu SMP PREEMPT_DYNAMIC Mon Apr 13 11:09:53 UTC 2026 x86_64 GNU/Linux
`df -h /`
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        30G  3.1G   27G  11% /
`free -h`
               total        used        free      shared  buff/cache   available
Mem:           3.8Gi       600Mi       1.5Gi       5.0Mi       2.0Gi       3.2Gi
Swap:             0B          0B          0B
`docker --version`
Docker version 29.1.3, build 29.1.3-0ubuntu4.1
`docker compose version`
Docker Compose version 2.40.3+ds1-0ubuntu1
- PASS: docker is usable by gtgb without sudo

## 2. Repository sync

Cloning into '/home/gtgb/omi-tasks-install-test-run/OMI-Tasks-Supabase'...
`git rev-parse --short HEAD`
b205d4b
`git log -1 --oneline`
b205d4b Initial OMI Tasks Supabase POC
- PASS: repository is clean after clone

## 3. Static package validation

`./scripts/validate_package.sh`
static_content_ok
compose_config_ok
schema_apply_skipped
package_validation_ok
- PASS: package validation reports ok

## 4. Installer install with local n8n

`./install.sh install --non-interactive --with-n8n`
Created /home/gtgb/omi-tasks-install-test-run/OMI-Tasks-Supabase/website/taskReviewUi/.env
 db Pulling 
 20f9cf2e9893 Pulling fs layer 
 6a0ac1617861 Pulling fs layer 
 c740b6b7dd0b Pulling fs layer 
 420ca0de84ca Pulling fs layer 
 0d3e610f9e0f Pulling fs layer 
 3b7e6bf074f6 Pulling fs layer 
 282a6867e326 Pulling fs layer 
 72393ada9150 Pulling fs layer 
 d9681cd68a94 Pulling fs layer 
 5ef55a6c860c Pulling fs layer 
 abdc7c6150b5 Pulling fs layer 
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 6a0ac1617861 Downloading [=============>                                     ]  1.049MB/3.864MB
 72393ada9150 Downloading [==================================================>]     169B/169B
 72393ada9150 Downloading [==================================================>]     169B/169B
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 72393ada9150 Downloading [==================================================>]     169B/169B
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 72393ada9150 Downloading [==================================================>]     169B/169B
 72393ada9150 Downloading [==================================================>]     169B/169B
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 420ca0de84ca Downloading [==================================================>]     971B/971B
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 420ca0de84ca Downloading [==================================================>]     971B/971B
 72393ada9150 Downloading [==================================================>]     169B/169B
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 420ca0de84ca Downloading [==================================================>]     971B/971B
 72393ada9150 Downloading [==================================================>]     169B/169B
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [>                                                  ]  2.097MB/105.2MB
 72393ada9150 Downloading [==================================================>]     169B/169B
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [=>                                                 ]  4.194MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 72393ada9150 Downloading [==================================================>]     169B/169B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [==>                                                ]  6.291MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 72393ada9150 Downloading [==================================================>]     169B/169B
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [====>                                              ]  9.437MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 72393ada9150 Downloading [==================================================>]     169B/169B
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [====>                                              ]  10.49MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 72393ada9150 Downloading [==================================================>]     169B/169B
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [=======>                                           ]  15.73MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 72393ada9150 Downloading [==================================================>]     169B/169B
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 0d3e610f9e0f Downloading [========>                                          ]  17.83MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 72393ada9150 Downloading [==================================================>]     169B/169B
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 fb2a3b9ecbd5 Downloading [==================================================>]  598.1kB/598.1kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 420ca0de84ca Downloading [==================================================>]     971B/971B
 9827fda4490e Downloading [==================================================>]  44.31kB/44.31kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [=========>                                         ]  19.92MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 72393ada9150 Downloading [==================================================>]     169B/169B
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 5ef55a6c860c Downloading [==================================================>]     169B/169B
 fb2a3b9ecbd5 Download complete 
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [==========>                                        ]  23.07MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 72393ada9150 Downloading [==================================================>]     169B/169B
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 5ef55a6c860c Downloading [==================================================>]     169B/169B
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [============>                                      ]  26.21MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 72393ada9150 Downloading [==================================================>]     169B/169B
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 5ef55a6c860c Downloading [==================================================>]     169B/169B
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 9827fda4490e Download complete 
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Downloading [==================================================>]  3.864MB/3.864MB
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [=============>                                     ]  28.31MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 5ef55a6c860c Downloading [==================================================>]     169B/169B
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 5ef55a6c860c Downloading [==================================================>]     169B/169B
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [==============>                                    ]  30.41MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 72393ada9150 Download complete 
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [===============>                                   ]  32.51MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 5ef55a6c860c Downloading [==================================================>]     169B/169B
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [===============>                                   ]  32.51MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 5ef55a6c860c Downloading [==================================================>]     169B/169B
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [===============>                                   ]  32.51MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 5ef55a6c860c Downloading [==================================================>]     169B/169B
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 c740b6b7dd0b Downloading [==================================================>]     114B/114B
 6a0ac1617861 Download complete 
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [================>                                  ]   34.6MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 5ef55a6c860c Downloading [==================================================>]     169B/169B
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 6a0ac1617861 Extracting 1 s
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 5ef55a6c860c Downloading [==================================================>]     169B/169B
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [==================>                                ]   38.8MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 6a0ac1617861 Extracting 1 s
 c740b6b7dd0b Download complete 
 420ca0de84ca Downloading [==================================================>]     971B/971B
 0d3e610f9e0f Downloading [====================>                              ]  44.04MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 5ef55a6c860c Downloading [==================================================>]     169B/169B
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 6a0ac1617861 Extracting 1 s
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 5ef55a6c860c Downloading [==================================================>]     169B/169B
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 420ca0de84ca Download complete 
 0d3e610f9e0f Downloading [=======================>                           ]  49.28MB/105.2MB
 3b7e6bf074f6 Downloading [==================================================>]  919.1kB/919.1kB
 282a6867e326 Downloading [==================================================>]  9.627kB/9.627kB
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 6a0ac1617861 Extracting 1 s
 0d3e610f9e0f Downloading [=========================>                         ]  54.53MB/105.2MB
 3b7e6bf074f6 Download complete 
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 5ef55a6c860c Downloading [==================================================>]     169B/169B
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 6a0ac1617861 Extracting 1 s
 5ef55a6c860c Downloading [==================================================>]     169B/169B
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 0d3e610f9e0f Downloading [============================>                      ]  59.77MB/105.2MB
 282a6867e326 Download complete 
 20f9cf2e9893 Downloading [==================================================>]     184B/184B
 d9681cd68a94 Downloading [==================================================>]     128B/128B
 6a0ac1617861 Extracting 1 s
 20f9cf2e9893 Download complete 
 5ef55a6c860c Downloading [==================================================>]     169B/169B
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 0d3e610f9e0f Downloading [==============================>                    ]  63.96MB/105.2MB
 6a0ac1617861 Extracting 1 s
 0d3e610f9e0f Downloading [==============================>                    ]  65.01MB/105.2MB
 d9681cd68a94 Download complete 
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 6a0ac1617861 Extracting 1 s
 5ef55a6c860c Download complete 
 abdc7c6150b5 Downloading [==================================================>]  6.096kB/6.096kB
 0d3e610f9e0f Downloading [==============================>                    ]  65.01MB/105.2MB
 6a0ac1617861 Extracting 1 s
 abdc7c6150b5 Download complete 
 0d3e610f9e0f Downloading [==============================>                    ]  65.01MB/105.2MB
 6a0ac1617861 Extracting 1 s
 0d3e610f9e0f Downloading [==============================>                    ]  65.01MB/105.2MB
 6a0ac1617861 Extracting 2 s
 0d3e610f9e0f Downloading [==============================>                    ]  65.01MB/105.2MB
 6a0ac1617861 Extracting 2 s
 0d3e610f9e0f Downloading [================================>                  ]  69.21MB/105.2MB
 6a0ac1617861 Extracting 2 s
 0d3e610f9e0f Downloading [==================================>                ]  72.35MB/105.2MB
 6a0ac1617861 Extracting 2 s
 0d3e610f9e0f Downloading [===================================>               ]   75.5MB/105.2MB
 6a0ac1617861 Extracting 2 s
 0d3e610f9e0f Downloading [=====================================>             ]  79.69MB/105.2MB
 6a0ac1617861 Extracting 2 s
 0d3e610f9e0f Downloading [=======================================>           ]  83.89MB/105.2MB
 0d3e610f9e0f Downloading [=========================================>         ]  88.08MB/105.2MB
 6a0ac1617861 Pull complete 
 0d3e610f9e0f Downloading [============================================>      ]  93.32MB/105.2MB
 420ca0de84ca Pull complete 
 3b7e6bf074f6 Extracting 1 s
 0d3e610f9e0f Downloading [============================================>      ]  94.37MB/105.2MB
 3b7e6bf074f6 Extracting 1 s
 0d3e610f9e0f Downloading [=============================================>     ]  95.42MB/105.2MB
 3b7e6bf074f6 Extracting 1 s
 0d3e610f9e0f Downloading [================================================>  ]  101.7MB/105.2MB
 0d3e610f9e0f Downloading [==================================================>]  105.2MB/105.2MB
 3b7e6bf074f6 Pull complete 
 0d3e610f9e0f Downloading [==================================================>]  105.2MB/105.2MB
 0d3e610f9e0f Downloading [==================================================>]  105.2MB/105.2MB
 0d3e610f9e0f Downloading [==================================================>]  105.2MB/105.2MB
 0d3e610f9e0f Downloading [==================================================>]  105.2MB/105.2MB
 0d3e610f9e0f Downloading [==================================================>]  105.2MB/105.2MB
 0d3e610f9e0f Downloading [==================================================>]  105.2MB/105.2MB
 0d3e610f9e0f Downloading [==================================================>]  105.2MB/105.2MB
 0d3e610f9e0f Downloading [==================================================>]  105.2MB/105.2MB
 72393ada9150 Extracting 1 s
 72393ada9150 Extracting 1 s
 0d3e610f9e0f Download complete 
 72393ada9150 Pull complete 
 c740b6b7dd0b Pull complete 
 0d3e610f9e0f Extracting 1 s
 0d3e610f9e0f Extracting 1 s
 0d3e610f9e0f Extracting 1 s
 0d3e610f9e0f Extracting 1 s
 0d3e610f9e0f Extracting 1 s
 0d3e610f9e0f Extracting 1 s
 0d3e610f9e0f Extracting 1 s
 0d3e610f9e0f Extracting 1 s
 0d3e610f9e0f Extracting 1 s
 0d3e610f9e0f Extracting 2 s
 0d3e610f9e0f Extracting 2 s
 0d3e610f9e0f Extracting 2 s
 0d3e610f9e0f Extracting 2 s
 0d3e610f9e0f Extracting 2 s
 0d3e610f9e0f Extracting 2 s
 0d3e610f9e0f Extracting 3 s
 0d3e610f9e0f Extracting 3 s
 0d3e610f9e0f Extracting 3 s
 0d3e610f9e0f Extracting 3 s
 0d3e610f9e0f Extracting 3 s
 0d3e610f9e0f Extracting 3 s
 0d3e610f9e0f Extracting 3 s
 0d3e610f9e0f Extracting 3 s
 0d3e610f9e0f Extracting 3 s
 0d3e610f9e0f Extracting 4 s
 0d3e610f9e0f Extracting 4 s
 0d3e610f9e0f Extracting 4 s
 0d3e610f9e0f Extracting 4 s
 0d3e610f9e0f Extracting 5 s
 0d3e610f9e0f Extracting 5 s
 0d3e610f9e0f Extracting 5 s
 0d3e610f9e0f Extracting 5 s
 0d3e610f9e0f Extracting 5 s
 0d3e610f9e0f Extracting 5 s
 0d3e610f9e0f Extracting 5 s
 0d3e610f9e0f Extracting 5 s
 0d3e610f9e0f Extracting 5 s
 0d3e610f9e0f Extracting 6 s
 0d3e610f9e0f Extracting 6 s
 0d3e610f9e0f Extracting 6 s
 0d3e610f9e0f Extracting 7 s
 0d3e610f9e0f Extracting 7 s
 0d3e610f9e0f Extracting 7 s
 0d3e610f9e0f Extracting 7 s
 0d3e610f9e0f Extracting 7 s
 0d3e610f9e0f Extracting 7 s
 0d3e610f9e0f Extracting 7 s
 0d3e610f9e0f Extracting 7 s
 0d3e610f9e0f Extracting 8 s
 0d3e610f9e0f Extracting 8 s
 0d3e610f9e0f Extracting 8 s
 0d3e610f9e0f Extracting 8 s
 0d3e610f9e0f Pull complete 
 282a6867e326 Extracting 1 s
 282a6867e326 Pull complete 
 d9681cd68a94 Pull complete 
 5ef55a6c860c Pull complete 
 abdc7c6150b5 Extracting 1 s
 abdc7c6150b5 Pull complete 
 20f9cf2e9893 Pull complete 
 db Pulled 
 Network omi-tasks-supabase_default  Creating
 Network omi-tasks-supabase_default  Created
 Container omi-tasks-supabase-test-db  Creating
 Container omi-tasks-supabase-test-db  Created
 Container omi-tasks-supabase-test-db  Starting
 Container omi-tasks-supabase-test-db  Started
Waiting for Postgres...
Applying database schema...
CREATE EXTENSION
CREATE SCHEMA
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE INDEX
INSERT 0 3
CREATE FUNCTION
DO
time="2026-05-10T22:06:04Z" level=warning msg="Docker Compose is configured to build using Bake, but buildx isn't installed"
#0 building with "default" instance using docker driver

#1 [omi-tasks-supabase-web internal] load build definition from Dockerfile
#1 transferring dockerfile:
#1 transferring dockerfile: 344B done
#1 DONE 1.0s

#2 [omi-tasks-supabase-web internal] load metadata for docker.io/library/python:3.12-slim
#2 DONE 2.0s

#3 [omi-tasks-supabase-web internal] load .dockerignore
#3 transferring context:
#3 transferring context: 2B done
#3 DONE 0.3s

#4 [omi-tasks-supabase-web internal] load build context
#4 transferring context: 19.28kB done
#4 DONE 0.7s

#5 [omi-tasks-supabase-web 1/5] FROM docker.io/library/python:3.12-slim@sha256:ec948fa5f90f4f8907e89f4800cfd2d2e91e391a4bce4a6afa77ba265bc3a2fe
#5 resolve docker.io/library/python:3.12-slim@sha256:ec948fa5f90f4f8907e89f4800cfd2d2e91e391a4bce4a6afa77ba265bc3a2fe 0.4s done
#5 DONE 1.5s

#5 [omi-tasks-supabase-web 1/5] FROM docker.io/library/python:3.12-slim@sha256:ec948fa5f90f4f8907e89f4800cfd2d2e91e391a4bce4a6afa77ba265bc3a2fe
#5 sha256:b33ff618953dcb6177e78bc33883a49817e571a1d9f0a3aa039e3228e0f21684 0B / 250B 0.2s
#5 sha256:b33ff618953dcb6177e78bc33883a49817e571a1d9f0a3aa039e3228e0f21684 250B / 250B 0.3s
#5 sha256:797809503061a7d1332e7b5c3df030896846f0a6a179f90060e85564dca1cf65 0B / 1.29MB 0.2s
#5 sha256:797809503061a7d1332e7b5c3df030896846f0a6a179f90060e85564dca1cf65 1.29MB / 1.29MB 0.5s
#5 sha256:759e0c85a86e6d82ceccf351143d3f4a17e4ba196c9684240898abe3b8ec13a9 0B / 12.11MB 0.2s
#5 sha256:b33ff618953dcb6177e78bc33883a49817e571a1d9f0a3aa039e3228e0f21684 250B / 250B 1.0s done
#5 sha256:797809503061a7d1332e7b5c3df030896846f0a6a179f90060e85564dca1cf65 1.29MB / 1.29MB 0.9s done
#5 sha256:759e0c85a86e6d82ceccf351143d3f4a17e4ba196c9684240898abe3b8ec13a9 2.10MB / 12.11MB 0.3s
#5 sha256:57fb71246055257a374deb7564ceca10f43c2352572b501efc08add5d24ebb61 0B / 29.78MB 0.3s
#5 sha256:759e0c85a86e6d82ceccf351143d3f4a17e4ba196c9684240898abe3b8ec13a9 5.24MB / 12.11MB 0.5s
#5 sha256:759e0c85a86e6d82ceccf351143d3f4a17e4ba196c9684240898abe3b8ec13a9 9.44MB / 12.11MB 0.6s
#5 sha256:57fb71246055257a374deb7564ceca10f43c2352572b501efc08add5d24ebb61 3.15MB / 29.78MB 0.6s
#5 sha256:759e0c85a86e6d82ceccf351143d3f4a17e4ba196c9684240898abe3b8ec13a9 12.11MB / 12.11MB 0.8s
#5 sha256:57fb71246055257a374deb7564ceca10f43c2352572b501efc08add5d24ebb61 8.39MB / 29.78MB 0.8s
#5 sha256:759e0c85a86e6d82ceccf351143d3f4a17e4ba196c9684240898abe3b8ec13a9 12.11MB / 12.11MB 0.9s done
#5 sha256:57fb71246055257a374deb7564ceca10f43c2352572b501efc08add5d24ebb61 15.73MB / 29.78MB 0.9s
#5 sha256:57fb71246055257a374deb7564ceca10f43c2352572b501efc08add5d24ebb61 20.97MB / 29.78MB 1.1s
#5 sha256:57fb71246055257a374deb7564ceca10f43c2352572b501efc08add5d24ebb61 29.36MB / 29.78MB 1.2s
#5 sha256:57fb71246055257a374deb7564ceca10f43c2352572b501efc08add5d24ebb61 29.78MB / 29.78MB 1.5s done
#5 extracting sha256:57fb71246055257a374deb7564ceca10f43c2352572b501efc08add5d24ebb61
#5 extracting sha256:57fb71246055257a374deb7564ceca10f43c2352572b501efc08add5d24ebb61 3.4s done
#5 DONE 7.6s

#5 [omi-tasks-supabase-web 1/5] FROM docker.io/library/python:3.12-slim@sha256:ec948fa5f90f4f8907e89f4800cfd2d2e91e391a4bce4a6afa77ba265bc3a2fe
#5 extracting sha256:797809503061a7d1332e7b5c3df030896846f0a6a179f90060e85564dca1cf65
#5 extracting sha256:797809503061a7d1332e7b5c3df030896846f0a6a179f90060e85564dca1cf65 0.4s done
#5 extracting sha256:759e0c85a86e6d82ceccf351143d3f4a17e4ba196c9684240898abe3b8ec13a9
#5 extracting sha256:759e0c85a86e6d82ceccf351143d3f4a17e4ba196c9684240898abe3b8ec13a9 1.3s done
#5 DONE 9.3s

#5 [omi-tasks-supabase-web 1/5] FROM docker.io/library/python:3.12-slim@sha256:ec948fa5f90f4f8907e89f4800cfd2d2e91e391a4bce4a6afa77ba265bc3a2fe
#5 extracting sha256:b33ff618953dcb6177e78bc33883a49817e571a1d9f0a3aa039e3228e0f21684
#5 extracting sha256:b33ff618953dcb6177e78bc33883a49817e571a1d9f0a3aa039e3228e0f21684 0.2s done
#5 DONE 9.5s

#6 [omi-tasks-supabase-web 2/5] WORKDIR /app
#6 DONE 1.3s

#7 [omi-tasks-supabase-web 3/5] COPY requirements.txt /app/requirements.txt
#7 DONE 0.6s

#8 [omi-tasks-supabase-web 4/5] RUN pip install --no-cache-dir -r /app/requirements.txt
#8 3.787 Collecting fastapi==0.115.6 (from -r /app/requirements.txt (line 1))
#8 3.971   Downloading fastapi-0.115.6-py3-none-any.whl.metadata (27 kB)
#8 4.120 Collecting uvicorn==0.34.0 (from uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 4.164   Downloading uvicorn-0.34.0-py3-none-any.whl.metadata (6.5 kB)
#8 4.231 Collecting psycopg==3.2.3 (from psycopg[binary]==3.2.3->-r /app/requirements.txt (line 3))
#8 4.275   Downloading psycopg-3.2.3-py3-none-any.whl.metadata (4.3 kB)
#8 4.331 Collecting python-multipart==0.0.20 (from -r /app/requirements.txt (line 4))
#8 4.375   Downloading python_multipart-0.0.20-py3-none-any.whl.metadata (1.8 kB)
#8 4.467 Collecting starlette<0.42.0,>=0.40.0 (from fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 4.503   Downloading starlette-0.41.3-py3-none-any.whl.metadata (6.0 kB)
#8 4.935 Collecting pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4 (from fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 4.967   Downloading pydantic-2.13.4-py3-none-any.whl.metadata (109 kB)
#8 5.069 Collecting typing-extensions>=4.8.0 (from fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 5.103   Downloading typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 kB)
#8 5.166 Collecting click>=7.0 (from uvicorn==0.34.0->uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 5.194   Downloading click-8.3.3-py3-none-any.whl.metadata (2.6 kB)
#8 5.235 Collecting h11>=0.8 (from uvicorn==0.34.0->uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 5.263   Downloading h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
#8 5.703 Collecting psycopg-binary==3.2.3 (from psycopg[binary]==3.2.3->-r /app/requirements.txt (line 3))
#8 5.734   Downloading psycopg_binary-3.2.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.8 kB)
#8 5.822 Collecting httptools>=0.6.3 (from uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 5.846   Downloading httptools-0.7.1-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (3.5 kB)
#8 5.908 Collecting python-dotenv>=0.13 (from uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 5.930   Downloading python_dotenv-1.2.2-py3-none-any.whl.metadata (27 kB)
#8 6.024 Collecting pyyaml>=5.1 (from uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 6.046   Downloading pyyaml-6.0.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.4 kB)
#8 6.155 Collecting uvloop!=0.15.0,!=0.15.1,>=0.14.0 (from uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 6.198   Downloading uvloop-0.22.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (4.9 kB)
#8 6.375 Collecting watchfiles>=0.13 (from uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 6.407   Downloading watchfiles-1.1.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.9 kB)
#8 6.622 Collecting websockets>=10.4 (from uvicorn[standard]==0.34.0->-r /app/requirements.txt (line 2))
#8 6.647   Downloading websockets-16.0-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (6.8 kB)
#8 6.683 Collecting annotated-types>=0.6.0 (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 6.723   Downloading annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
#8 9.000 Collecting pydantic-core==2.46.4 (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 9.031   Downloading pydantic_core-2.46.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.6 kB)
#8 9.074 Collecting typing-inspection>=0.4.2 (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 9.102   Downloading typing_inspection-0.4.2-py3-none-any.whl.metadata (2.6 kB)
#8 9.170 Collecting anyio<5,>=3.4.0 (from starlette<0.42.0,>=0.40.0->fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 9.190   Downloading anyio-4.13.0-py3-none-any.whl.metadata (4.5 kB)
#8 9.263 Collecting idna>=2.8 (from anyio<5,>=3.4.0->starlette<0.42.0,>=0.40.0->fastapi==0.115.6->-r /app/requirements.txt (line 1))
#8 9.291   Downloading idna-3.14-py3-none-any.whl.metadata (8.0 kB)
#8 9.351 Downloading fastapi-0.115.6-py3-none-any.whl (94 kB)
#8 9.386 Downloading uvicorn-0.34.0-py3-none-any.whl (62 kB)
#8 9.415 Downloading psycopg-3.2.3-py3-none-any.whl (197 kB)
#8 9.450 Downloading python_multipart-0.0.20-py3-none-any.whl (24 kB)
#8 9.479 Downloading psycopg_binary-3.2.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (4.2 MB)
#8 9.670    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.2/4.2 MB 22.3 MB/s eta 0:00:00
#8 9.695 Downloading click-8.3.3-py3-none-any.whl (110 kB)
#8 9.727 Downloading h11-0.16.0-py3-none-any.whl (37 kB)
#8 9.755 Downloading httptools-0.7.1-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (517 kB)
#8 9.807 Downloading pydantic-2.13.4-py3-none-any.whl (472 kB)
#8 9.867 Downloading pydantic_core-2.46.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
#8 10.05    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 11.0 MB/s eta 0:00:00
#8 10.08 Downloading python_dotenv-1.2.2-py3-none-any.whl (22 kB)
#8 10.11 Downloading pyyaml-6.0.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (807 kB)
#8 10.19    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 807.9/807.9 kB 10.2 MB/s eta 0:00:00
#8 10.21 Downloading starlette-0.41.3-py3-none-any.whl (73 kB)
#8 10.25 Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
#8 10.28 Downloading uvloop-0.22.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (4.4 MB)
#8 10.80    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.4/4.4 MB 8.9 MB/s eta 0:00:00
#8 10.83 Downloading watchfiles-1.1.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (456 kB)
#8 10.91 Downloading websockets-16.0-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (184 kB)
#8 10.96 Downloading annotated_types-0.7.0-py3-none-any.whl (13 kB)
#8 10.99 Downloading anyio-4.13.0-py3-none-any.whl (114 kB)
#8 11.03 Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)
#8 11.06 Downloading idna-3.14-py3-none-any.whl (72 kB)
#8 11.24 Installing collected packages: websockets, uvloop, typing-extensions, pyyaml, python-multipart, python-dotenv, psycopg-binary, idna, httptools, h11, click, annotated-types, uvicorn, typing-inspection, pydantic-core, psycopg, anyio, watchfiles, starlette, pydantic, fastapi
#8 15.60 Successfully installed annotated-types-0.7.0 anyio-4.13.0 click-8.3.3 fastapi-0.115.6 h11-0.16.0 httptools-0.7.1 idna-3.14 psycopg-3.2.3 psycopg-binary-3.2.3 pydantic-2.13.4 pydantic-core-2.46.4 python-dotenv-1.2.2 python-multipart-0.0.20 pyyaml-6.0.3 starlette-0.41.3 typing-extensions-4.15.0 typing-inspection-0.4.2 uvicorn-0.34.0 uvloop-0.22.1 watchfiles-1.1.1 websockets-16.0
#8 15.60 WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
#8 15.81 
#8 15.81 [notice] A new release of pip is available: 25.0.1 -> 26.1.1
#8 15.81 [notice] To update, run: pip install --upgrade pip
#8 DONE 16.8s

#9 [omi-tasks-supabase-web 5/5] COPY app.py /app/app.py
#9 DONE 0.6s

#10 [omi-tasks-supabase-web] exporting to image
#10 exporting layers
#10 exporting layers 5.8s done
#10 exporting manifest sha256:f593083ca81a2b9008db1da2b4a1f2162c98a8893d6a3b6aabb81cdc0e4457d3
#10 exporting manifest sha256:f593083ca81a2b9008db1da2b4a1f2162c98a8893d6a3b6aabb81cdc0e4457d3 0.2s done
#10 exporting config sha256:5d69fc448d1c09fef5da9db3347a6a0417f54c3dc651f9ac6c847e81212c0502
#10 exporting config sha256:5d69fc448d1c09fef5da9db3347a6a0417f54c3dc651f9ac6c847e81212c0502 0.2s done
#10 exporting attestation manifest sha256:376ce43d176e8795cab21b2f04d9873ad35c0bd474f591b2e3e5d8081971c0f6
#10 exporting attestation manifest sha256:376ce43d176e8795cab21b2f04d9873ad35c0bd474f591b2e3e5d8081971c0f6 0.4s done
#10 exporting manifest list sha256:c97603824d48fbaa27fa3a3ee79e1ab18df664b2f4741cb67956a30e509a7fc0
#10 exporting manifest list sha256:c97603824d48fbaa27fa3a3ee79e1ab18df664b2f4741cb67956a30e509a7fc0 0.2s done
#10 naming to docker.io/library/omi-tasks-supabase-omi-tasks-supabase-web:latest
#10 naming to docker.io/library/omi-tasks-supabase-omi-tasks-supabase-web:latest 0.0s done
#10 unpacking to docker.io/library/omi-tasks-supabase-omi-tasks-supabase-web:latest
#10 unpacking to docker.io/library/omi-tasks-supabase-omi-tasks-supabase-web:latest 2.3s done
#10 DONE 9.4s

#11 [omi-tasks-supabase-web] resolving provenance for metadata file
#11 DONE 0.0s
 omi-tasks-supabase-web  Built
time="2026-05-10T22:06:48Z" level=warning msg="Found orphan containers ([omi-tasks-supabase-test-db]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up."
 Container omi-tasks-supabase-web  Creating
 Container omi-tasks-supabase-web  Created
 Container omi-tasks-supabase-web  Starting
 Container omi-tasks-supabase-web  Started
 omi-tasks-supabase-n8n Pulling 
 b0f1a56d391d Pulling fs layer 
 ba8e56425256 Pulling fs layer 
 721755724bcf Pulling fs layer 
 c9368855797a Pulling fs layer 
 32bea4346786 Pulling fs layer 
 f5f617bfda84 Pulling fs layer 
 4f4fb700ef54 Pulling fs layer 
 4f4fb700ef54 Pulling fs layer 
 d3eb7cad75f8 Pulling fs layer 
 466817520ca7 Pulling fs layer 
 0690af90bffe Pulling fs layer 
 7c3151e3fbac Pulling fs layer 
 0929a2dec4be Downloading [========>                                          ]  1.049MB/6.202MB
 0929a2dec4be Downloading [================>                                  ]  2.097MB/6.202MB
 0929a2dec4be Downloading [==========================================>        ]  5.243MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 c9368855797a Downloading [=>                                                 ]  1.049MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 c9368855797a Downloading [==>                                                ]  2.097MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 c9368855797a Downloading [==>                                                ]  2.097MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 c9368855797a Downloading [===>                                               ]  3.146MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 721755724bcf Downloading [==================================================>]     371B/371B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 c9368855797a Downloading [=======>                                           ]  6.291MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 721755724bcf Downloading [==================================================>]     371B/371B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 c9368855797a Downloading [=========>                                         ]  8.389MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 721755724bcf Downloading [==================================================>]     371B/371B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 ba8e56425256 Downloading [==================================================>]   1.88kB/1.88kB
 c9368855797a Downloading [==============>                                    ]  12.58MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 721755724bcf Downloading [==================================================>]     371B/371B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 ba8e56425256 Downloading [==================================================>]   1.88kB/1.88kB
 c9368855797a Downloading [==================>                                ]  15.73MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 721755724bcf Downloading [==================================================>]     371B/371B
 721755724bcf Downloading [==================================================>]     371B/371B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 ba8e56425256 Downloading [==================================================>]   1.88kB/1.88kB
 f5f617bfda84 Downloading [=====>                                             ]  2.097MB/20.3MB
 c9368855797a Downloading [===================>                               ]  16.78MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 ba8e56425256 Downloading [==================================================>]   1.88kB/1.88kB
 f5f617bfda84 Downloading [=======>                                           ]  3.146MB/20.3MB
 c9368855797a Downloading [=====================>                             ]  17.83MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 721755724bcf Downloading [==================================================>]     371B/371B
 c9368855797a Downloading [=======================>                           ]  19.92MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 4f4fb700ef54 Downloading [==================================================>]      32B/32B
 721755724bcf Downloading [==================================================>]     371B/371B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 ba8e56425256 Downloading [==================================================>]   1.88kB/1.88kB
 f5f617bfda84 Downloading [============>                                      ]  5.243MB/20.3MB
 ba8e56425256 Downloading [==================================================>]   1.88kB/1.88kB
 f5f617bfda84 Downloading [============>                                      ]  5.243MB/20.3MB
 466817520ca7 Downloading [==================================================>]     311B/311B
 c9368855797a Downloading [==========================>                        ]  22.02MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 4f4fb700ef54 Downloading [==================================================>]      32B/32B
 721755724bcf Downloading [==================================================>]     371B/371B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 c9368855797a Downloading [==========================>                        ]  22.02MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 4f4fb700ef54 Downloading [==================================================>]      32B/32B
 d3eb7cad75f8 Downloading [>                                                  ]  1.049MB/250.8MB
 721755724bcf Downloading [==================================================>]     371B/371B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 ba8e56425256 Downloading [==================================================>]   1.88kB/1.88kB
 f5f617bfda84 Downloading [============>                                      ]  5.243MB/20.3MB
 466817520ca7 Downloading [==================================================>]     311B/311B
 466817520ca7 Downloading [==================================================>]     311B/311B
 c9368855797a Downloading [==========================>                        ]  22.02MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 4f4fb700ef54 Downloading [==================================================>]      32B/32B
 d3eb7cad75f8 Downloading [>                                                  ]  1.049MB/250.8MB
 721755724bcf Downloading [==================================================>]     371B/371B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 ba8e56425256 Downloading [==================================================>]   1.88kB/1.88kB
 f5f617bfda84 Downloading [============>                                      ]  5.243MB/20.3MB
 b0f1a56d391d Downloading [==================================================>]     244B/244B
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 ba8e56425256 Downloading [==================================================>]   1.88kB/1.88kB
 f5f617bfda84 Downloading [===============>                                   ]  6.291MB/20.3MB
 466817520ca7 Downloading [==================================================>]     311B/311B
 c9368855797a Downloading [==========================>                        ]  22.02MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 4f4fb700ef54 Downloading [==================================================>]      32B/32B
 d3eb7cad75f8 Downloading [>                                                  ]  1.049MB/250.8MB
 721755724bcf Downloading [==================================================>]     371B/371B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 c9368855797a Downloading [===========================>                       ]  23.07MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 4f4fb700ef54 Downloading [==================================================>]      32B/32B
 d3eb7cad75f8 Downloading [>                                                  ]  2.097MB/250.8MB
 721755724bcf Downloading [==================================================>]     371B/371B
 0929a2dec4be Downloading [==================================================>]  6.202MB/6.202MB
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 ba8e56425256 Downloading [==================================================>]   1.88kB/1.88kB
 f5f617bfda84 Downloading [====================>                              ]  8.389MB/20.3MB
 466817520ca7 Downloading [==================================================>]     311B/311B
 c9368855797a Downloading [===============================>                   ]  26.21MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 4f4fb700ef54 Downloading [==================================================>]      32B/32B
 d3eb7cad75f8 Downloading [>                                                  ]  2.097MB/250.8MB
 721755724bcf Downloading [==================================================>]     371B/371B
 b0f1a56d391d Download complete 
 0690af90bffe Downloading [==================================================>]  6.079kB/6.079kB
 ba8e56425256 Downloading [==================================================>]   1.88kB/1.88kB
 f5f617bfda84 Downloading [=========================>                         ]  10.49MB/20.3MB
 466817520ca7 Downloading [==================================================>]     311B/311B
 721755724bcf Downloading [==================================================>]     371B/371B
 0929a2dec4be Download complete 
 ba8e56425256 Downloading [==================================================>]   1.88kB/1.88kB
 f5f617bfda84 Downloading [==============================>                    ]  12.58MB/20.3MB
 466817520ca7 Downloading [==================================================>]     311B/311B
 c9368855797a Downloading [====================================>              ]  30.41MB/42.16MB
 32bea4346786 Downloading [==================================================>]      76B/76B
 4f4fb700ef54 Downloading [==================================================>]      32B/32B
 d3eb7cad75f8 Downloading [>                                                  ]  2.097MB/250.8MB
 0690af90bffe Download complete 
 ba8e56425256 Downloading [==================================================>]   1.88kB/1.88kB
 f5f617bfda84 Downloading [==============================>                    ]  12.58MB/20.3MB
 466817520ca7 Downloading [==================================================>]     311B/311B
 c9368855797a Downloading [====================================>              ]  30.41MB/42.16MB
 4f4fb700ef54 Downloading [==================================================>]      32B/32B
 d3eb7cad75f8 Downloading [>                                                  ]  3.146MB/250.8MB
 721755724bcf Downloading [==================================================>]     371B/371B
 ba8e56425256 Downloading [==================================================>]   1.88kB/1.88kB
 f5f617bfda84 Downloading [====================================>              ]  14.68MB/20.3MB
 466817520ca7 Downloading [==================================================>]     311B/311B
 c9368855797a Downloading [====================================>              ]  30.41MB/42.16MB
 32bea4346786 Download complete 
 4f4fb700ef54 Downloading [==================================================>]      32B/32B
 d3eb7cad75f8 Downloading [>                                                  ]  4.194MB/250.8MB
 466817520ca7 Downloading [==================================================>]     311B/311B
 c9368855797a Downloading [====================================>              ]  30.41MB/42.16MB
 4f4fb700ef54 Downloading [==================================================>]      32B/32B
 d3eb7cad75f8 Downloading [>                                                  ]  4.194MB/250.8MB
 721755724bcf Download complete 
 f5f617bfda84 Downloading [======================================>            ]  15.73MB/20.3MB
 ba8e56425256 Download complete 
 f5f617bfda84 Downloading [======================================>            ]  15.73MB/20.3MB
 466817520ca7 Downloading [==================================================>]     311B/311B
 c9368855797a Downloading [====================================>              ]  30.41MB/42.16MB
 d3eb7cad75f8 Downloading [=>                                                 ]  5.243MB/250.8MB
 ba8e56425256 Extracting 1 s
 d3eb7cad75f8 Downloading [=>                                                 ]  5.243MB/250.8MB
 f5f617bfda84 Downloading [======================================>            ]  15.73MB/20.3MB
 466817520ca7 Download complete 
 c9368855797a Downloading [====================================>              ]  30.41MB/42.16MB
 4f4fb700ef54 Download complete 
 ba8e56425256 Extracting 1 s
 f5f617bfda84 Downloading [======================================>            ]  15.73MB/20.3MB
 c9368855797a Downloading [======================================>            ]  32.51MB/42.16MB
 d3eb7cad75f8 Downloading [=>                                                 ]  5.243MB/250.8MB
 ba8e56425256 Extracting 1 s
 f5f617bfda84 Downloading [==============================================>    ]  18.87MB/20.3MB
 c9368855797a Downloading [======================================>            ]  32.51MB/42.16MB
 d3eb7cad75f8 Downloading [=>                                                 ]  6.291MB/250.8MB
 ba8e56425256 Extracting 1 s
 f5f617bfda84 Downloading [==================================================>]   20.3MB/20.3MB
 c9368855797a Downloading [=======================================>           ]  33.55MB/42.16MB
 d3eb7cad75f8 Downloading [=>                                                 ]   7.34MB/250.8MB
 ba8e56425256 Extracting 1 s
 f5f617bfda84 Downloading [==================================================>]   20.3MB/20.3MB
 c9368855797a Downloading [==========================================>        ]  35.65MB/42.16MB
 d3eb7cad75f8 Downloading [==>                                                ]  10.49MB/250.8MB
 ba8e56425256 Extracting 1 s
 f5f617bfda84 Downloading [==================================================>]   20.3MB/20.3MB
 c9368855797a Downloading [================================================>  ]  40.89MB/42.16MB
 d3eb7cad75f8 Downloading [==>                                                ]  13.63MB/250.8MB
 7c3151e3fbac Downloading [=====>                                             ]  1.049MB/9.541MB
 ba8e56425256 Extracting 1 s
 d3eb7cad75f8 Downloading [==>                                                ]  14.68MB/250.8MB
 7c3151e3fbac Downloading [=====>                                             ]  1.049MB/9.541MB
 f5f617bfda84 Downloading [==================================================>]   20.3MB/20.3MB
 c9368855797a Downloading [==================================================>]  42.16MB/42.16MB
 ba8e56425256 Extracting 1 s
 f5f617bfda84 Downloading [==================================================>]   20.3MB/20.3MB
 c9368855797a Downloading [==================================================>]  42.16MB/42.16MB
 d3eb7cad75f8 Downloading [===>                                               ]  16.78MB/250.8MB
 7c3151e3fbac Downloading [=====>                                             ]  1.049MB/9.541MB
 ba8e56425256 Extracting 1 s
 7c3151e3fbac Downloading [=====>                                             ]  1.049MB/9.541MB
 f5f617bfda84 Downloading [==================================================>]   20.3MB/20.3MB
 c9368855797a Downloading [==================================================>]  42.16MB/42.16MB
 d3eb7cad75f8 Downloading [===>                                               ]  16.78MB/250.8MB
 ba8e56425256 Extracting 1 s
 d3eb7cad75f8 Downloading [===>                                               ]  19.92MB/250.8MB
 7c3151e3fbac Downloading [=====>                                             ]  1.049MB/9.541MB
 f5f617bfda84 Downloading [==================================================>]   20.3MB/20.3MB
 c9368855797a Downloading [==================================================>]  42.16MB/42.16MB
 ba8e56425256 Extracting 1 s
 d3eb7cad75f8 Downloading [====>                                              ]  22.02MB/250.8MB
 7c3151e3fbac Downloading [=====>                                             ]  1.049MB/9.541MB
 f5f617bfda84 Downloading [==================================================>]   20.3MB/20.3MB
 c9368855797a Downloading [==================================================>]  42.16MB/42.16MB
 ba8e56425256 Extracting 2 s
 f5f617bfda84 Downloading [==================================================>]   20.3MB/20.3MB
 c9368855797a Downloading [==================================================>]  42.16MB/42.16MB
 d3eb7cad75f8 Downloading [====>                                              ]  24.12MB/250.8MB
 7c3151e3fbac Downloading [=====>                                             ]  1.049MB/9.541MB
 ba8e56425256 Pull complete 
 d3eb7cad75f8 Downloading [=====>                                             ]  25.17MB/250.8MB
 7c3151e3fbac Downloading [=====>                                             ]  1.049MB/9.541MB
 f5f617bfda84 Download complete 
 c9368855797a Download complete 
 d3eb7cad75f8 Downloading [=====>                                             ]  27.26MB/250.8MB
 7c3151e3fbac Downloading [=====>                                             ]  1.049MB/9.541MB
 d3eb7cad75f8 Downloading [=====>                                             ]  28.31MB/250.8MB
 7c3151e3fbac Downloading [=====>                                             ]  1.049MB/9.541MB
 d3eb7cad75f8 Downloading [======>                                            ]  30.41MB/250.8MB
 7c3151e3fbac Downloading [==========>                                        ]  2.097MB/9.541MB
 d3eb7cad75f8 Downloading [======>                                            ]  33.55MB/250.8MB
 7c3151e3fbac Downloading [==========>                                        ]  2.097MB/9.541MB
 7c3151e3fbac Downloading [==========>                                        ]  2.097MB/9.541MB
 d3eb7cad75f8 Downloading [=======>                                           ]  35.65MB/250.8MB
 d3eb7cad75f8 Downloading [=======>                                           ]  37.75MB/250.8MB
 7c3151e3fbac Downloading [==========>                                        ]  2.097MB/9.541MB
 d3eb7cad75f8 Downloading [=======>                                           ]  39.85MB/250.8MB
 7c3151e3fbac Downloading [==========>                                        ]  2.097MB/9.541MB
 d3eb7cad75f8 Downloading [========>                                          ]  42.99MB/250.8MB
 7c3151e3fbac Downloading [==========>                                        ]  2.097MB/9.541MB
 d3eb7cad75f8 Downloading [=========>                                         ]  46.14MB/250.8MB
 7c3151e3fbac Downloading [================>                                  ]  3.146MB/9.541MB
 d3eb7cad75f8 Downloading [=========>                                         ]  48.23MB/250.8MB
 7c3151e3fbac Downloading [================>                                  ]  3.146MB/9.541MB
 7c3151e3fbac Downloading [================>                                  ]  3.146MB/9.541MB
 d3eb7cad75f8 Downloading [==========>                                        ]  51.38MB/250.8MB
 d3eb7cad75f8 Downloading [==========>                                        ]  54.53MB/250.8MB
 7c3151e3fbac Downloading [================>                                  ]  3.146MB/9.541MB
 7c3151e3fbac Downloading [=====================>                             ]  4.194MB/9.541MB
 d3eb7cad75f8 Downloading [===========>                                       ]  57.67MB/250.8MB
 d3eb7cad75f8 Downloading [============>                                      ]  60.82MB/250.8MB
 7c3151e3fbac Downloading [=====================>                             ]  4.194MB/9.541MB
 d3eb7cad75f8 Downloading [============>                                      ]  62.91MB/250.8MB
 7c3151e3fbac Downloading [=====================>                             ]  4.194MB/9.541MB
 d3eb7cad75f8 Downloading [============>                                      ]  65.01MB/250.8MB
 7c3151e3fbac Downloading [===========================>                       ]  5.243MB/9.541MB
 d3eb7cad75f8 Downloading [=============>                                     ]  68.16MB/250.8MB
 7c3151e3fbac Downloading [===========================>                       ]  5.243MB/9.541MB
 d3eb7cad75f8 Downloading [=============>                                     ]  69.21MB/250.8MB
 7c3151e3fbac Downloading [===========================>                       ]  5.243MB/9.541MB
 d3eb7cad75f8 Downloading [==============>                                    ]  74.45MB/250.8MB
 7c3151e3fbac Downloading [================================>                  ]  6.291MB/9.541MB
 d3eb7cad75f8 Downloading [===============>                                   ]  77.59MB/250.8MB
 7c3151e3fbac Downloading [================================>                  ]  6.291MB/9.541MB
 d3eb7cad75f8 Downloading [================>                                  ]  80.74MB/250.8MB
 7c3151e3fbac Downloading [================================>                  ]  6.291MB/9.541MB
 d3eb7cad75f8 Downloading [================>                                  ]  83.89MB/250.8MB
 7c3151e3fbac Downloading [======================================>            ]   7.34MB/9.541MB
 d3eb7cad75f8 Downloading [=================>                                 ]  85.98MB/250.8MB
 7c3151e3fbac Downloading [======================================>            ]   7.34MB/9.541MB
 d3eb7cad75f8 Downloading [=================>                                 ]  88.08MB/250.8MB
 7c3151e3fbac Downloading [======================================>            ]   7.34MB/9.541MB
 d3eb7cad75f8 Downloading [==================>                                ]  92.27MB/250.8MB
 7c3151e3fbac Downloading [===========================================>       ]  8.389MB/9.541MB
 d3eb7cad75f8 Downloading [===================>                               ]  96.47MB/250.8MB
 7c3151e3fbac Downloading [===========================================>       ]  8.389MB/9.541MB
 7c3151e3fbac Downloading [==================================================>]  9.541MB/9.541MB
 d3eb7cad75f8 Downloading [===================>                               ]  98.57MB/250.8MB
 d3eb7cad75f8 Downloading [===================>                               ]  99.61MB/250.8MB
 7c3151e3fbac Downloading [==================================================>]  9.541MB/9.541MB
 d3eb7cad75f8 Downloading [===================>                               ]  99.61MB/250.8MB
 7c3151e3fbac Downloading [==================================================>]  9.541MB/9.541MB
 d3eb7cad75f8 Downloading [===================>                               ]  99.61MB/250.8MB
 7c3151e3fbac Downloading [==================================================>]  9.541MB/9.541MB
 d3eb7cad75f8 Downloading [====================>                              ]  102.8MB/250.8MB
 d3eb7cad75f8 Downloading [=====================>                             ]    107MB/250.8MB
 7c3151e3fbac Download complete 
 7c3151e3fbac Extracting 1 s
 d3eb7cad75f8 Downloading [=====================>                             ]  109.1MB/250.8MB
 7c3151e3fbac Extracting 1 s
 d3eb7cad75f8 Downloading [======================>                            ]  113.2MB/250.8MB
 7c3151e3fbac Extracting 1 s
 d3eb7cad75f8 Downloading [======================>                            ]  114.3MB/250.8MB
 7c3151e3fbac Extracting 1 s
 d3eb7cad75f8 Downloading [=======================>                           ]  116.4MB/250.8MB
 7c3151e3fbac Extracting 1 s
 d3eb7cad75f8 Downloading [========================>                          ]  120.6MB/250.8MB
 7c3151e3fbac Extracting 1 s
 d3eb7cad75f8 Downloading [========================>                          ]  123.7MB/250.8MB
 7c3151e3fbac Pull complete 
 d3eb7cad75f8 Downloading [=========================>                         ]  127.9MB/250.8MB
 d3eb7cad75f8 Downloading [==========================>                        ]  131.1MB/250.8MB
 721755724bcf Extracting 1 s
 d3eb7cad75f8 Downloading [==========================>                        ]  133.2MB/250.8MB
 d3eb7cad75f8 Downloading [===========================>                       ]  136.3MB/250.8MB
 721755724bcf Pull complete 
 d3eb7cad75f8 Downloading [============================>                      ]  140.5MB/250.8MB
 c9368855797a Extracting 1 s
 d3eb7cad75f8 Downloading [============================>                      ]  142.6MB/250.8MB
 c9368855797a Extracting 1 s
 d3eb7cad75f8 Downloading [=============================>                     ]  146.8MB/250.8MB
 c9368855797a Extracting 1 s
 d3eb7cad75f8 Downloading [=============================>                     ]  147.8MB/250.8MB
 c9368855797a Extracting 1 s
 d3eb7cad75f8 Downloading [==============================>                    ]    152MB/250.8MB
 c9368855797a Extracting 1 s
 d3eb7cad75f8 Downloading [==============================>                    ]  154.1MB/250.8MB
 c9368855797a Extracting 1 s
 d3eb7cad75f8 Downloading [===============================>                   ]  157.3MB/250.8MB
 c9368855797a Extracting 1 s
 d3eb7cad75f8 Downloading [================================>                  ]  162.5MB/250.8MB
 c9368855797a Extracting 1 s
 d3eb7cad75f8 Downloading [================================>                  ]  162.5MB/250.8MB
 c9368855797a Extracting 1 s
 d3eb7cad75f8 Downloading [================================>                  ]  164.6MB/250.8MB
 c9368855797a Extracting 1 s
 d3eb7cad75f8 Downloading [=================================>                 ]  168.8MB/250.8MB
 c9368855797a Extracting 2 s
 d3eb7cad75f8 Downloading [==================================>                ]    172MB/250.8MB
 c9368855797a Extracting 2 s
 d3eb7cad75f8 Downloading [===================================>               ]  176.2MB/250.8MB
 c9368855797a Extracting 2 s
 d3eb7cad75f8 Downloading [===================================>               ]  180.4MB/250.8MB
 c9368855797a Extracting 2 s
 d3eb7cad75f8 Downloading [====================================>              ]  184.5MB/250.8MB
 c9368855797a Extracting 2 s
 d3eb7cad75f8 Downloading [=====================================>             ]  186.6MB/250.8MB
 c9368855797a Extracting 2 s
 d3eb7cad75f8 Downloading [======================================>            ]  191.9MB/250.8MB
 c9368855797a Extracting 2 s
 d3eb7cad75f8 Downloading [======================================>            ]    194MB/250.8MB
 c9368855797a Extracting 2 s
 d3eb7cad75f8 Downloading [=======================================>           ]  198.2MB/250.8MB
 c9368855797a Extracting 2 s
 d3eb7cad75f8 Downloading [=======================================>           ]  200.3MB/250.8MB
 c9368855797a Extracting 2 s
 d3eb7cad75f8 Downloading [========================================>          ]  202.4MB/250.8MB
 c9368855797a Extracting 3 s
 d3eb7cad75f8 Downloading [=========================================>         ]  207.6MB/250.8MB
 c9368855797a Extracting 3 s
 d3eb7cad75f8 Downloading [=========================================>         ]  209.7MB/250.8MB
 c9368855797a Extracting 3 s
 d3eb7cad75f8 Downloading [==========================================>        ]  213.9MB/250.8MB
 c9368855797a Extracting 3 s
 d3eb7cad75f8 Downloading [===========================================>       ]  218.1MB/250.8MB
 c9368855797a Extracting 3 s
 d3eb7cad75f8 Downloading [============================================>      ]  221.2MB/250.8MB
 c9368855797a Extracting 3 s
 d3eb7cad75f8 Downloading [============================================>      ]  223.3MB/250.8MB
 c9368855797a Extracting 3 s
 d3eb7cad75f8 Downloading [============================================>      ]  224.4MB/250.8MB
 c9368855797a Extracting 3 s
 d3eb7cad75f8 Downloading [=============================================>     ]  228.6MB/250.8MB
 c9368855797a Extracting 3 s
 d3eb7cad75f8 Downloading [=============================================>     ]  229.6MB/250.8MB
 c9368855797a Extracting 3 s
 d3eb7cad75f8 Downloading [==============================================>    ]  231.7MB/250.8MB
 c9368855797a Extracting 4 s
 d3eb7cad75f8 Downloading [==============================================>    ]  233.8MB/250.8MB
 c9368855797a Extracting 4 s
 d3eb7cad75f8 Downloading [==============================================>    ]  234.9MB/250.8MB
 c9368855797a Extracting 4 s
 d3eb7cad75f8 Downloading [===============================================>   ]    238MB/250.8MB
 c9368855797a Extracting 4 s
 d3eb7cad75f8 Downloading [===============================================>   ]    238MB/250.8MB
 c9368855797a Extracting 4 s
 d3eb7cad75f8 Downloading [================================================>  ]  242.2MB/250.8MB
 d3eb7cad75f8 Downloading [=================================================> ]  246.4MB/250.8MB
 d3eb7cad75f8 Downloading [=================================================> ]  247.5MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 c9368855797a Pull complete 
 d3eb7cad75f8 Downloading [==================================================>]  250.8MB/250.8MB
 d3eb7cad75f8 Download complete 
 32bea4346786 Extracting 1 s
 32bea4346786 Pull complete 
 0690af90bffe Pull complete 
 f5f617bfda84 Extracting 1 s
 f5f617bfda84 Extracting 1 s
 f5f617bfda84 Extracting 1 s
 f5f617bfda84 Extracting 1 s
 f5f617bfda84 Extracting 1 s
 f5f617bfda84 Extracting 1 s
 f5f617bfda84 Extracting 1 s
 f5f617bfda84 Extracting 1 s
 f5f617bfda84 Extracting 1 s
 f5f617bfda84 Extracting 1 s
 f5f617bfda84 Extracting 1 s
 f5f617bfda84 Pull complete 
 4f4fb700ef54 Extracting 1 s
 4f4fb700ef54 Extracting 1 s
 4f4fb700ef54 Pull complete 
 d3eb7cad75f8 Extracting 1 s
 d3eb7cad75f8 Extracting 1 s
 d3eb7cad75f8 Extracting 1 s
 d3eb7cad75f8 Extracting 1 s
 d3eb7cad75f8 Extracting 1 s
 d3eb7cad75f8 Extracting 1 s
 d3eb7cad75f8 Extracting 1 s
 d3eb7cad75f8 Extracting 1 s
 d3eb7cad75f8 Extracting 1 s
 d3eb7cad75f8 Extracting 1 s
 d3eb7cad75f8 Extracting 1 s
 d3eb7cad75f8 Extracting 2 s
 d3eb7cad75f8 Extracting 2 s
 d3eb7cad75f8 Extracting 2 s
 d3eb7cad75f8 Extracting 2 s
 d3eb7cad75f8 Extracting 2 s
 d3eb7cad75f8 Extracting 2 s
 d3eb7cad75f8 Extracting 2 s
 d3eb7cad75f8 Extracting 2 s
 d3eb7cad75f8 Extracting 2 s
 d3eb7cad75f8 Extracting 2 s
 d3eb7cad75f8 Extracting 3 s
 d3eb7cad75f8 Extracting 3 s
 d3eb7cad75f8 Extracting 3 s
 d3eb7cad75f8 Extracting 3 s
 d3eb7cad75f8 Extracting 3 s
 d3eb7cad75f8 Extracting 3 s
 d3eb7cad75f8 Extracting 3 s
 d3eb7cad75f8 Extracting 3 s
 d3eb7cad75f8 Extracting 3 s
 d3eb7cad75f8 Extracting 3 s
 d3eb7cad75f8 Extracting 4 s
 d3eb7cad75f8 Extracting 4 s
 d3eb7cad75f8 Extracting 4 s
 d3eb7cad75f8 Extracting 4 s
 d3eb7cad75f8 Extracting 4 s
 d3eb7cad75f8 Extracting 4 s
 d3eb7cad75f8 Extracting 4 s
 d3eb7cad75f8 Extracting 4 s
 d3eb7cad75f8 Extracting 4 s
 d3eb7cad75f8 Extracting 4 s
 d3eb7cad75f8 Extracting 5 s
 d3eb7cad75f8 Extracting 5 s
 d3eb7cad75f8 Extracting 5 s
 d3eb7cad75f8 Extracting 5 s
 d3eb7cad75f8 Extracting 5 s
 d3eb7cad75f8 Extracting 5 s
 d3eb7cad75f8 Extracting 5 s
 d3eb7cad75f8 Extracting 5 s
 d3eb7cad75f8 Extracting 5 s
 d3eb7cad75f8 Extracting 5 s
 d3eb7cad75f8 Extracting 6 s
 d3eb7cad75f8 Extracting 6 s
 d3eb7cad75f8 Extracting 6 s
 d3eb7cad75f8 Extracting 6 s
 d3eb7cad75f8 Extracting 6 s
 d3eb7cad75f8 Extracting 6 s
 d3eb7cad75f8 Extracting 6 s
 d3eb7cad75f8 Extracting 6 s
 d3eb7cad75f8 Extracting 6 s
 d3eb7cad75f8 Extracting 7 s
 d3eb7cad75f8 Extracting 7 s
 d3eb7cad75f8 Extracting 7 s
 d3eb7cad75f8 Extracting 7 s
 d3eb7cad75f8 Extracting 7 s
 d3eb7cad75f8 Extracting 7 s
 d3eb7cad75f8 Extracting 7 s
 d3eb7cad75f8 Extracting 7 s
 d3eb7cad75f8 Extracting 7 s
 d3eb7cad75f8 Extracting 7 s
 d3eb7cad75f8 Extracting 7 s
 d3eb7cad75f8 Extracting 8 s
 d3eb7cad75f8 Extracting 8 s
 d3eb7cad75f8 Extracting 8 s
 d3eb7cad75f8 Extracting 8 s
 d3eb7cad75f8 Extracting 8 s
 d3eb7cad75f8 Extracting 8 s
 d3eb7cad75f8 Extracting 8 s
 d3eb7cad75f8 Extracting 8 s
 d3eb7cad75f8 Extracting 8 s
 d3eb7cad75f8 Extracting 8 s
 d3eb7cad75f8 Extracting 9 s
 d3eb7cad75f8 Extracting 9 s
 d3eb7cad75f8 Extracting 9 s
 d3eb7cad75f8 Extracting 9 s
 d3eb7cad75f8 Extracting 9 s
 d3eb7cad75f8 Extracting 9 s
 d3eb7cad75f8 Extracting 9 s
 d3eb7cad75f8 Extracting 9 s
 d3eb7cad75f8 Extracting 9 s
 d3eb7cad75f8 Extracting 9 s
 d3eb7cad75f8 Extracting 10 s
 d3eb7cad75f8 Extracting 10 s
 d3eb7cad75f8 Extracting 10 s
 d3eb7cad75f8 Extracting 10 s
 d3eb7cad75f8 Extracting 10 s
 d3eb7cad75f8 Extracting 10 s
 d3eb7cad75f8 Extracting 10 s
 d3eb7cad75f8 Extracting 10 s
 d3eb7cad75f8 Extracting 10 s
 d3eb7cad75f8 Extracting 10 s
 d3eb7cad75f8 Extracting 11 s
 d3eb7cad75f8 Extracting 11 s
 d3eb7cad75f8 Extracting 11 s
 d3eb7cad75f8 Extracting 11 s
 d3eb7cad75f8 Extracting 11 s
 d3eb7cad75f8 Extracting 11 s
 d3eb7cad75f8 Extracting 11 s
 d3eb7cad75f8 Extracting 11 s
 d3eb7cad75f8 Extracting 11 s
 d3eb7cad75f8 Extracting 12 s
 d3eb7cad75f8 Extracting 12 s
 d3eb7cad75f8 Extracting 12 s
 d3eb7cad75f8 Extracting 12 s
 d3eb7cad75f8 Extracting 12 s
 d3eb7cad75f8 Extracting 12 s
 d3eb7cad75f8 Extracting 12 s
 d3eb7cad75f8 Extracting 12 s
 d3eb7cad75f8 Extracting 12 s
 d3eb7cad75f8 Extracting 12 s
 d3eb7cad75f8 Extracting 12 s
 d3eb7cad75f8 Extracting 13 s
 d3eb7cad75f8 Extracting 13 s
 d3eb7cad75f8 Extracting 13 s
 d3eb7cad75f8 Extracting 13 s
 d3eb7cad75f8 Extracting 13 s
 d3eb7cad75f8 Extracting 13 s
 d3eb7cad75f8 Extracting 13 s
 d3eb7cad75f8 Extracting 13 s
 d3eb7cad75f8 Extracting 13 s
 d3eb7cad75f8 Extracting 13 s
 d3eb7cad75f8 Extracting 14 s
 d3eb7cad75f8 Extracting 14 s
 d3eb7cad75f8 Extracting 14 s
 d3eb7cad75f8 Extracting 14 s
 d3eb7cad75f8 Extracting 14 s
 d3eb7cad75f8 Extracting 14 s
 d3eb7cad75f8 Extracting 14 s
 d3eb7cad75f8 Extracting 14 s
 d3eb7cad75f8 Extracting 14 s
 d3eb7cad75f8 Extracting 14 s
 d3eb7cad75f8 Extracting 15 s
 d3eb7cad75f8 Extracting 15 s
 d3eb7cad75f8 Extracting 15 s
 d3eb7cad75f8 Extracting 15 s
 d3eb7cad75f8 Extracting 15 s
 d3eb7cad75f8 Extracting 15 s
 d3eb7cad75f8 Extracting 15 s
 d3eb7cad75f8 Extracting 15 s
 d3eb7cad75f8 Extracting 15 s
 d3eb7cad75f8 Extracting 16 s
 d3eb7cad75f8 Extracting 16 s
 d3eb7cad75f8 Extracting 16 s
 d3eb7cad75f8 Extracting 16 s
 d3eb7cad75f8 Extracting 16 s
 d3eb7cad75f8 Extracting 16 s
 d3eb7cad75f8 Extracting 16 s
 d3eb7cad75f8 Extracting 16 s
 d3eb7cad75f8 Extracting 16 s
 d3eb7cad75f8 Extracting 16 s
 d3eb7cad75f8 Extracting 16 s
 d3eb7cad75f8 Extracting 17 s
 d3eb7cad75f8 Extracting 17 s
 d3eb7cad75f8 Extracting 17 s
 d3eb7cad75f8 Extracting 17 s
 d3eb7cad75f8 Extracting 17 s
 d3eb7cad75f8 Extracting 17 s
 d3eb7cad75f8 Extracting 17 s
 d3eb7cad75f8 Extracting 17 s
 d3eb7cad75f8 Extracting 17 s
 d3eb7cad75f8 Extracting 17 s
 d3eb7cad75f8 Extracting 18 s
 d3eb7cad75f8 Extracting 18 s
 d3eb7cad75f8 Extracting 18 s
 d3eb7cad75f8 Extracting 18 s
 d3eb7cad75f8 Extracting 18 s
 d3eb7cad75f8 Extracting 18 s
 d3eb7cad75f8 Extracting 18 s
 d3eb7cad75f8 Extracting 18 s
 d3eb7cad75f8 Extracting 18 s
 d3eb7cad75f8 Extracting 18 s
 d3eb7cad75f8 Extracting 19 s
 d3eb7cad75f8 Extracting 19 s
 d3eb7cad75f8 Extracting 19 s
 d3eb7cad75f8 Extracting 19 s
 d3eb7cad75f8 Extracting 19 s
 d3eb7cad75f8 Extracting 19 s
 d3eb7cad75f8 Extracting 19 s
 d3eb7cad75f8 Extracting 19 s
 d3eb7cad75f8 Extracting 19 s
 d3eb7cad75f8 Extracting 20 s
 d3eb7cad75f8 Extracting 20 s
 d3eb7cad75f8 Extracting 20 s
 d3eb7cad75f8 Extracting 20 s
 d3eb7cad75f8 Extracting 20 s
 d3eb7cad75f8 Extracting 20 s
 d3eb7cad75f8 Extracting 20 s
 d3eb7cad75f8 Extracting 20 s
 d3eb7cad75f8 Extracting 20 s
 d3eb7cad75f8 Extracting 20 s
 d3eb7cad75f8 Extracting 20 s
 d3eb7cad75f8 Extracting 21 s
 d3eb7cad75f8 Extracting 21 s
 d3eb7cad75f8 Extracting 21 s
 d3eb7cad75f8 Extracting 21 s
 d3eb7cad75f8 Extracting 21 s
 d3eb7cad75f8 Extracting 21 s
 d3eb7cad75f8 Extracting 21 s
 d3eb7cad75f8 Extracting 21 s
 d3eb7cad75f8 Extracting 21 s
 d3eb7cad75f8 Extracting 21 s
 d3eb7cad75f8 Extracting 22 s
 d3eb7cad75f8 Extracting 22 s
 d3eb7cad75f8 Extracting 22 s
 d3eb7cad75f8 Extracting 22 s
 d3eb7cad75f8 Extracting 22 s
 d3eb7cad75f8 Extracting 22 s
 d3eb7cad75f8 Extracting 22 s
 d3eb7cad75f8 Extracting 22 s
 d3eb7cad75f8 Extracting 22 s
 d3eb7cad75f8 Extracting 22 s
 d3eb7cad75f8 Extracting 23 s
 d3eb7cad75f8 Extracting 23 s
 d3eb7cad75f8 Extracting 23 s
 d3eb7cad75f8 Extracting 23 s
 d3eb7cad75f8 Extracting 23 s
 d3eb7cad75f8 Extracting 23 s
 d3eb7cad75f8 Extracting 23 s
 d3eb7cad75f8 Extracting 23 s
 d3eb7cad75f8 Extracting 23 s
 d3eb7cad75f8 Extracting 23 s
 d3eb7cad75f8 Extracting 24 s
 d3eb7cad75f8 Extracting 24 s
 d3eb7cad75f8 Extracting 24 s
 d3eb7cad75f8 Extracting 24 s
 d3eb7cad75f8 Extracting 24 s
 d3eb7cad75f8 Extracting 24 s
 d3eb7cad75f8 Extracting 24 s
 d3eb7cad75f8 Extracting 24 s
 d3eb7cad75f8 Extracting 24 s
 d3eb7cad75f8 Extracting 24 s
 d3eb7cad75f8 Extracting 25 s
 d3eb7cad75f8 Extracting 25 s
 d3eb7cad75f8 Extracting 25 s
 d3eb7cad75f8 Extracting 25 s
 d3eb7cad75f8 Extracting 25 s
 d3eb7cad75f8 Extracting 25 s
 d3eb7cad75f8 Extracting 25 s
 d3eb7cad75f8 Extracting 25 s
 d3eb7cad75f8 Extracting 25 s
 d3eb7cad75f8 Extracting 25 s
 d3eb7cad75f8 Extracting 26 s
 d3eb7cad75f8 Extracting 26 s
 d3eb7cad75f8 Extracting 26 s
 d3eb7cad75f8 Extracting 26 s
 d3eb7cad75f8 Extracting 26 s
 d3eb7cad75f8 Extracting 26 s
 d3eb7cad75f8 Extracting 26 s
 d3eb7cad75f8 Extracting 26 s
 d3eb7cad75f8 Extracting 26 s
 d3eb7cad75f8 Extracting 27 s
 d3eb7cad75f8 Extracting 27 s
 d3eb7cad75f8 Extracting 27 s
 d3eb7cad75f8 Extracting 27 s
 d3eb7cad75f8 Extracting 27 s
 d3eb7cad75f8 Extracting 27 s
 d3eb7cad75f8 Extracting 27 s
 d3eb7cad75f8 Extracting 27 s
 d3eb7cad75f8 Extracting 27 s
 d3eb7cad75f8 Extracting 27 s
 d3eb7cad75f8 Extracting 27 s
 d3eb7cad75f8 Extracting 28 s
 d3eb7cad75f8 Extracting 28 s
 d3eb7cad75f8 Extracting 28 s
 d3eb7cad75f8 Extracting 28 s
 d3eb7cad75f8 Extracting 28 s
 d3eb7cad75f8 Extracting 28 s
 d3eb7cad75f8 Extracting 28 s
 d3eb7cad75f8 Extracting 28 s
 d3eb7cad75f8 Extracting 28 s
 d3eb7cad75f8 Extracting 29 s
 d3eb7cad75f8 Extracting 29 s
 d3eb7cad75f8 Extracting 29 s
 d3eb7cad75f8 Extracting 29 s
 d3eb7cad75f8 Extracting 29 s
 d3eb7cad75f8 Extracting 29 s
 d3eb7cad75f8 Extracting 29 s
 d3eb7cad75f8 Extracting 29 s
 d3eb7cad75f8 Extracting 29 s
 d3eb7cad75f8 Extracting 29 s
 d3eb7cad75f8 Extracting 29 s
 d3eb7cad75f8 Extracting 30 s
 d3eb7cad75f8 Extracting 30 s
 d3eb7cad75f8 Extracting 30 s
 d3eb7cad75f8 Extracting 30 s
 d3eb7cad75f8 Extracting 30 s
 d3eb7cad75f8 Extracting 30 s
 d3eb7cad75f8 Extracting 30 s
 d3eb7cad75f8 Extracting 30 s
 d3eb7cad75f8 Extracting 30 s
 d3eb7cad75f8 Extracting 30 s
 d3eb7cad75f8 Extracting 31 s
 d3eb7cad75f8 Extracting 31 s
 d3eb7cad75f8 Extracting 31 s
 d3eb7cad75f8 Extracting 31 s
 d3eb7cad75f8 Extracting 31 s
 d3eb7cad75f8 Extracting 31 s
 d3eb7cad75f8 Extracting 31 s
 d3eb7cad75f8 Extracting 31 s
 d3eb7cad75f8 Extracting 31 s
 d3eb7cad75f8 Extracting 31 s
 d3eb7cad75f8 Extracting 32 s
 d3eb7cad75f8 Extracting 32 s
 d3eb7cad75f8 Extracting 32 s
 d3eb7cad75f8 Extracting 32 s
 d3eb7cad75f8 Extracting 32 s
 d3eb7cad75f8 Extracting 32 s
 d3eb7cad75f8 Extracting 32 s
 d3eb7cad75f8 Extracting 32 s
 d3eb7cad75f8 Extracting 32 s
 d3eb7cad75f8 Extracting 32 s
 d3eb7cad75f8 Extracting 33 s
 d3eb7cad75f8 Extracting 33 s
 d3eb7cad75f8 Extracting 33 s
 d3eb7cad75f8 Extracting 33 s
 d3eb7cad75f8 Extracting 33 s
 d3eb7cad75f8 Extracting 33 s
 d3eb7cad75f8 Extracting 33 s
 d3eb7cad75f8 Extracting 33 s
 d3eb7cad75f8 Extracting 33 s
 d3eb7cad75f8 Extracting 33 s
 d3eb7cad75f8 Extracting 34 s
 d3eb7cad75f8 Extracting 34 s
 d3eb7cad75f8 Extracting 34 s
 d3eb7cad75f8 Extracting 34 s
 d3eb7cad75f8 Extracting 34 s
 d3eb7cad75f8 Extracting 34 s
 d3eb7cad75f8 Extracting 34 s
 d3eb7cad75f8 Extracting 34 s
 d3eb7cad75f8 Extracting 34 s
 d3eb7cad75f8 Extracting 35 s
 d3eb7cad75f8 Extracting 35 s
 d3eb7cad75f8 Extracting 35 s
 d3eb7cad75f8 Extracting 35 s
 d3eb7cad75f8 Extracting 35 s
 d3eb7cad75f8 Extracting 35 s
 d3eb7cad75f8 Extracting 35 s
 d3eb7cad75f8 Extracting 35 s
 d3eb7cad75f8 Extracting 35 s
 d3eb7cad75f8 Extracting 35 s
 d3eb7cad75f8 Extracting 35 s
 d3eb7cad75f8 Extracting 36 s
 d3eb7cad75f8 Extracting 36 s
 d3eb7cad75f8 Extracting 36 s
 d3eb7cad75f8 Extracting 36 s
 d3eb7cad75f8 Extracting 36 s
 d3eb7cad75f8 Extracting 36 s
 d3eb7cad75f8 Extracting 36 s
 d3eb7cad75f8 Extracting 36 s
 d3eb7cad75f8 Extracting 36 s
 d3eb7cad75f8 Extracting 36 s
 d3eb7cad75f8 Extracting 37 s
 d3eb7cad75f8 Extracting 37 s
 d3eb7cad75f8 Extracting 37 s
 d3eb7cad75f8 Extracting 37 s
 d3eb7cad75f8 Extracting 37 s
 d3eb7cad75f8 Extracting 37 s
 d3eb7cad75f8 Extracting 37 s
 d3eb7cad75f8 Extracting 37 s
 d3eb7cad75f8 Extracting 37 s
 d3eb7cad75f8 Extracting 38 s
 d3eb7cad75f8 Extracting 38 s
 d3eb7cad75f8 Extracting 38 s
 d3eb7cad75f8 Extracting 38 s
 d3eb7cad75f8 Extracting 38 s
 d3eb7cad75f8 Extracting 38 s
 d3eb7cad75f8 Extracting 38 s
 d3eb7cad75f8 Extracting 38 s
 d3eb7cad75f8 Extracting 38 s
 d3eb7cad75f8 Extracting 38 s
 d3eb7cad75f8 Extracting 38 s
 d3eb7cad75f8 Extracting 39 s
 d3eb7cad75f8 Extracting 39 s
 d3eb7cad75f8 Extracting 39 s
 d3eb7cad75f8 Extracting 39 s
 d3eb7cad75f8 Extracting 39 s
 d3eb7cad75f8 Extracting 39 s
 d3eb7cad75f8 Extracting 39 s
 d3eb7cad75f8 Extracting 39 s
 d3eb7cad75f8 Extracting 39 s
 d3eb7cad75f8 Extracting 40 s
 d3eb7cad75f8 Extracting 40 s
 d3eb7cad75f8 Extracting 40 s
 d3eb7cad75f8 Extracting 40 s
 d3eb7cad75f8 Extracting 40 s
 d3eb7cad75f8 Extracting 40 s
 d3eb7cad75f8 Extracting 40 s
 d3eb7cad75f8 Extracting 40 s
 d3eb7cad75f8 Extracting 40 s
 d3eb7cad75f8 Extracting 40 s
 d3eb7cad75f8 Extracting 40 s
 d3eb7cad75f8 Extracting 41 s
 d3eb7cad75f8 Extracting 41 s
 d3eb7cad75f8 Extracting 41 s
 d3eb7cad75f8 Extracting 41 s
 d3eb7cad75f8 Extracting 41 s
 d3eb7cad75f8 Extracting 41 s
 d3eb7cad75f8 Extracting 41 s
 d3eb7cad75f8 Extracting 41 s
 d3eb7cad75f8 Extracting 41 s
 d3eb7cad75f8 Extracting 42 s
 d3eb7cad75f8 Extracting 42 s
 d3eb7cad75f8 Extracting 42 s
 d3eb7cad75f8 Extracting 42 s
 d3eb7cad75f8 Extracting 42 s
 d3eb7cad75f8 Extracting 42 s
 d3eb7cad75f8 Extracting 42 s
 d3eb7cad75f8 Extracting 42 s
 d3eb7cad75f8 Extracting 42 s
 d3eb7cad75f8 Extracting 42 s
 d3eb7cad75f8 Extracting 42 s
 d3eb7cad75f8 Extracting 43 s
 d3eb7cad75f8 Extracting 43 s
 d3eb7cad75f8 Extracting 43 s
 d3eb7cad75f8 Extracting 43 s
 d3eb7cad75f8 Extracting 43 s
 d3eb7cad75f8 Extracting 43 s
 d3eb7cad75f8 Extracting 43 s
 d3eb7cad75f8 Extracting 43 s
 d3eb7cad75f8 Extracting 43 s
 d3eb7cad75f8 Extracting 43 s
 d3eb7cad75f8 Extracting 44 s
 d3eb7cad75f8 Extracting 44 s
 d3eb7cad75f8 Extracting 44 s
 d3eb7cad75f8 Extracting 44 s
 d3eb7cad75f8 Extracting 44 s
 d3eb7cad75f8 Extracting 44 s
 d3eb7cad75f8 Extracting 44 s
 d3eb7cad75f8 Extracting 44 s
 d3eb7cad75f8 Extracting 44 s
 d3eb7cad75f8 Extracting 45 s
 d3eb7cad75f8 Extracting 45 s
 d3eb7cad75f8 Extracting 45 s
 d3eb7cad75f8 Extracting 45 s
 d3eb7cad75f8 Extracting 45 s
 d3eb7cad75f8 Extracting 45 s
 d3eb7cad75f8 Extracting 45 s
 d3eb7cad75f8 Extracting 45 s
 d3eb7cad75f8 Extracting 45 s
 d3eb7cad75f8 Extracting 45 s
 d3eb7cad75f8 Extracting 45 s
 d3eb7cad75f8 Extracting 46 s
 d3eb7cad75f8 Extracting 46 s
 d3eb7cad75f8 Extracting 46 s
 d3eb7cad75f8 Extracting 46 s
 d3eb7cad75f8 Extracting 46 s
 d3eb7cad75f8 Extracting 46 s
 d3eb7cad75f8 Extracting 46 s
 d3eb7cad75f8 Extracting 46 s
 d3eb7cad75f8 Extracting 46 s
 d3eb7cad75f8 Extracting 46 s
 d3eb7cad75f8 Extracting 47 s
 d3eb7cad75f8 Extracting 47 s
 d3eb7cad75f8 Extracting 47 s
 d3eb7cad75f8 Extracting 47 s
 d3eb7cad75f8 Extracting 47 s
 d3eb7cad75f8 Extracting 47 s
 d3eb7cad75f8 Extracting 47 s
 d3eb7cad75f8 Extracting 47 s
 d3eb7cad75f8 Extracting 47 s
 d3eb7cad75f8 Extracting 47 s
 d3eb7cad75f8 Extracting 48 s
 d3eb7cad75f8 Extracting 48 s
 d3eb7cad75f8 Extracting 48 s
 d3eb7cad75f8 Extracting 48 s
 d3eb7cad75f8 Extracting 48 s
 d3eb7cad75f8 Extracting 48 s
 d3eb7cad75f8 Extracting 48 s
 d3eb7cad75f8 Extracting 48 s
 d3eb7cad75f8 Extracting 48 s
 d3eb7cad75f8 Extracting 48 s
 d3eb7cad75f8 Extracting 49 s
 d3eb7cad75f8 Extracting 49 s
 d3eb7cad75f8 Extracting 49 s
 d3eb7cad75f8 Extracting 49 s
 d3eb7cad75f8 Extracting 49 s
 d3eb7cad75f8 Extracting 49 s
 d3eb7cad75f8 Extracting 49 s
 d3eb7cad75f8 Extracting 49 s
 d3eb7cad75f8 Extracting 49 s
 d3eb7cad75f8 Extracting 49 s
 d3eb7cad75f8 Extracting 50 s
 d3eb7cad75f8 Extracting 50 s
 d3eb7cad75f8 Extracting 50 s
 d3eb7cad75f8 Extracting 50 s
 d3eb7cad75f8 Extracting 50 s
 d3eb7cad75f8 Extracting 50 s
 d3eb7cad75f8 Extracting 50 s
 d3eb7cad75f8 Extracting 50 s
 d3eb7cad75f8 Extracting 50 s
 d3eb7cad75f8 Extracting 50 s
 d3eb7cad75f8 Extracting 51 s
 d3eb7cad75f8 Extracting 51 s
 d3eb7cad75f8 Extracting 51 s
 d3eb7cad75f8 Extracting 51 s
 d3eb7cad75f8 Extracting 51 s
 d3eb7cad75f8 Extracting 51 s
 d3eb7cad75f8 Extracting 51 s
 d3eb7cad75f8 Extracting 51 s
 d3eb7cad75f8 Extracting 51 s
 d3eb7cad75f8 Extracting 51 s
 d3eb7cad75f8 Extracting 52 s
 d3eb7cad75f8 Extracting 52 s
 d3eb7cad75f8 Extracting 52 s
 d3eb7cad75f8 Extracting 52 s
 d3eb7cad75f8 Extracting 52 s
 d3eb7cad75f8 Extracting 52 s
 d3eb7cad75f8 Extracting 52 s
 d3eb7cad75f8 Extracting 52 s
 d3eb7cad75f8 Extracting 52 s
 d3eb7cad75f8 Extracting 52 s
 d3eb7cad75f8 Extracting 53 s
 d3eb7cad75f8 Extracting 53 s
 d3eb7cad75f8 Extracting 53 s
 d3eb7cad75f8 Extracting 53 s
 d3eb7cad75f8 Extracting 53 s
 d3eb7cad75f8 Extracting 53 s
 d3eb7cad75f8 Extracting 53 s
 d3eb7cad75f8 Extracting 53 s
 d3eb7cad75f8 Extracting 53 s
 d3eb7cad75f8 Extracting 53 s
 d3eb7cad75f8 Extracting 54 s
 d3eb7cad75f8 Extracting 54 s
 d3eb7cad75f8 Extracting 54 s
 d3eb7cad75f8 Extracting 54 s
 d3eb7cad75f8 Extracting 54 s
 d3eb7cad75f8 Extracting 54 s
 d3eb7cad75f8 Extracting 54 s
 d3eb7cad75f8 Extracting 54 s
 d3eb7cad75f8 Extracting 54 s
 d3eb7cad75f8 Extracting 55 s
 d3eb7cad75f8 Extracting 55 s
 d3eb7cad75f8 Extracting 55 s
 d3eb7cad75f8 Extracting 55 s
 d3eb7cad75f8 Extracting 55 s
 d3eb7cad75f8 Extracting 55 s
 d3eb7cad75f8 Extracting 55 s
 d3eb7cad75f8 Extracting 55 s
 d3eb7cad75f8 Extracting 55 s
 d3eb7cad75f8 Extracting 55 s
 d3eb7cad75f8 Extracting 55 s
 d3eb7cad75f8 Extracting 56 s
 d3eb7cad75f8 Extracting 56 s
 d3eb7cad75f8 Extracting 56 s
 d3eb7cad75f8 Extracting 56 s
 d3eb7cad75f8 Extracting 56 s
 d3eb7cad75f8 Extracting 56 s
 d3eb7cad75f8 Extracting 56 s
 d3eb7cad75f8 Extracting 56 s
 d3eb7cad75f8 Extracting 56 s
 d3eb7cad75f8 Extracting 56 s
 d3eb7cad75f8 Extracting 57 s
 d3eb7cad75f8 Extracting 57 s
 d3eb7cad75f8 Extracting 57 s
 d3eb7cad75f8 Extracting 57 s
 d3eb7cad75f8 Extracting 57 s
 d3eb7cad75f8 Extracting 57 s
 d3eb7cad75f8 Extracting 57 s
 d3eb7cad75f8 Extracting 57 s
 d3eb7cad75f8 Extracting 57 s
 d3eb7cad75f8 Extracting 58 s
 d3eb7cad75f8 Extracting 58 s
 d3eb7cad75f8 Extracting 58 s
 d3eb7cad75f8 Extracting 58 s
 d3eb7cad75f8 Extracting 58 s
 d3eb7cad75f8 Extracting 58 s
 d3eb7cad75f8 Extracting 58 s
 d3eb7cad75f8 Extracting 58 s
 d3eb7cad75f8 Extracting 58 s
 d3eb7cad75f8 Extracting 58 s
 d3eb7cad75f8 Extracting 59 s
 d3eb7cad75f8 Extracting 59 s
 d3eb7cad75f8 Extracting 59 s
 d3eb7cad75f8 Extracting 59 s
 d3eb7cad75f8 Extracting 59 s
 d3eb7cad75f8 Extracting 59 s
 d3eb7cad75f8 Extracting 59 s
 d3eb7cad75f8 Extracting 59 s
 d3eb7cad75f8 Extracting 59 s
 d3eb7cad75f8 Extracting 59 s
 d3eb7cad75f8 Extracting 59 s
 d3eb7cad75f8 Extracting 60 s
 d3eb7cad75f8 Extracting 60 s
 d3eb7cad75f8 Extracting 60 s
 d3eb7cad75f8 Extracting 60 s
 d3eb7cad75f8 Extracting 60 s
 d3eb7cad75f8 Extracting 60 s
 d3eb7cad75f8 Extracting 60 s
 d3eb7cad75f8 Extracting 60 s
 d3eb7cad75f8 Extracting 60 s
 d3eb7cad75f8 Extracting 60 s
 d3eb7cad75f8 Extracting 61 s
 d3eb7cad75f8 Extracting 61 s
 d3eb7cad75f8 Extracting 61 s
 d3eb7cad75f8 Extracting 61 s
 d3eb7cad75f8 Extracting 61 s
 d3eb7cad75f8 Extracting 61 s
 d3eb7cad75f8 Extracting 61 s
 d3eb7cad75f8 Extracting 61 s
 d3eb7cad75f8 Extracting 61 s
 d3eb7cad75f8 Extracting 61 s
 d3eb7cad75f8 Extracting 62 s
 d3eb7cad75f8 Extracting 62 s
 d3eb7cad75f8 Extracting 62 s
 d3eb7cad75f8 Extracting 62 s
 d3eb7cad75f8 Extracting 62 s
 d3eb7cad75f8 Extracting 62 s
 d3eb7cad75f8 Extracting 62 s
 d3eb7cad75f8 Extracting 62 s
 d3eb7cad75f8 Extracting 62 s
 d3eb7cad75f8 Extracting 63 s
 d3eb7cad75f8 Extracting 63 s
 d3eb7cad75f8 Extracting 63 s
 d3eb7cad75f8 Extracting 63 s
 d3eb7cad75f8 Extracting 63 s
 d3eb7cad75f8 Extracting 63 s
 d3eb7cad75f8 Extracting 63 s
 d3eb7cad75f8 Extracting 63 s
 d3eb7cad75f8 Extracting 63 s
 d3eb7cad75f8 Extracting 63 s
 d3eb7cad75f8 Extracting 63 s
 d3eb7cad75f8 Extracting 64 s
 d3eb7cad75f8 Extracting 64 s
 d3eb7cad75f8 Extracting 64 s
 d3eb7cad75f8 Extracting 64 s
 d3eb7cad75f8 Extracting 64 s
 d3eb7cad75f8 Extracting 64 s
 d3eb7cad75f8 Extracting 64 s
 d3eb7cad75f8 Extracting 64 s
 d3eb7cad75f8 Extracting 64 s
 d3eb7cad75f8 Extracting 64 s
 d3eb7cad75f8 Extracting 65 s
 d3eb7cad75f8 Extracting 65 s
 d3eb7cad75f8 Extracting 65 s
 d3eb7cad75f8 Extracting 65 s
 d3eb7cad75f8 Extracting 65 s
 d3eb7cad75f8 Extracting 65 s
 d3eb7cad75f8 Extracting 65 s
 d3eb7cad75f8 Extracting 65 s
 d3eb7cad75f8 Extracting 65 s
 d3eb7cad75f8 Extracting 65 s
 d3eb7cad75f8 Extracting 66 s
 d3eb7cad75f8 Extracting 66 s
 d3eb7cad75f8 Extracting 66 s
 d3eb7cad75f8 Extracting 66 s
 d3eb7cad75f8 Extracting 66 s
 d3eb7cad75f8 Extracting 66 s
 d3eb7cad75f8 Extracting 66 s
 d3eb7cad75f8 Extracting 66 s
 d3eb7cad75f8 Extracting 66 s
 d3eb7cad75f8 Extracting 66 s
 d3eb7cad75f8 Extracting 67 s
 d3eb7cad75f8 Extracting 67 s
 d3eb7cad75f8 Extracting 67 s
 d3eb7cad75f8 Extracting 67 s
 d3eb7cad75f8 Extracting 67 s
 d3eb7cad75f8 Extracting 67 s
 d3eb7cad75f8 Extracting 67 s
 d3eb7cad75f8 Extracting 67 s
 d3eb7cad75f8 Extracting 67 s
 d3eb7cad75f8 Extracting 67 s
 d3eb7cad75f8 Extracting 68 s
 d3eb7cad75f8 Extracting 68 s
 d3eb7cad75f8 Extracting 68 s
 d3eb7cad75f8 Extracting 68 s
 d3eb7cad75f8 Extracting 68 s
 d3eb7cad75f8 Extracting 68 s
 d3eb7cad75f8 Extracting 68 s
 d3eb7cad75f8 Extracting 68 s
 d3eb7cad75f8 Extracting 68 s
 d3eb7cad75f8 Extracting 69 s
 d3eb7cad75f8 Extracting 69 s
 d3eb7cad75f8 Extracting 69 s
 d3eb7cad75f8 Extracting 69 s
 d3eb7cad75f8 Extracting 69 s
 d3eb7cad75f8 Extracting 69 s
 d3eb7cad75f8 Extracting 69 s
 d3eb7cad75f8 Extracting 69 s
 d3eb7cad75f8 Extracting 69 s
 d3eb7cad75f8 Extracting 69 s
 d3eb7cad75f8 Extracting 69 s
 d3eb7cad75f8 Extracting 70 s
 d3eb7cad75f8 Extracting 70 s
 d3eb7cad75f8 Extracting 70 s
 d3eb7cad75f8 Extracting 70 s
 d3eb7cad75f8 Extracting 70 s
 d3eb7cad75f8 Extracting 70 s
 d3eb7cad75f8 Extracting 70 s
 d3eb7cad75f8 Extracting 70 s
 d3eb7cad75f8 Extracting 70 s
 d3eb7cad75f8 Extracting 70 s
 d3eb7cad75f8 Extracting 71 s
 d3eb7cad75f8 Extracting 71 s
 d3eb7cad75f8 Extracting 71 s
 d3eb7cad75f8 Extracting 71 s
 d3eb7cad75f8 Extracting 71 s
 d3eb7cad75f8 Extracting 71 s
 d3eb7cad75f8 Extracting 71 s
 d3eb7cad75f8 Extracting 71 s
 d3eb7cad75f8 Extracting 71 s
 d3eb7cad75f8 Extracting 71 s
 d3eb7cad75f8 Extracting 72 s
 d3eb7cad75f8 Extracting 72 s
 d3eb7cad75f8 Extracting 72 s
 d3eb7cad75f8 Extracting 72 s
 d3eb7cad75f8 Extracting 72 s
 d3eb7cad75f8 Extracting 72 s
 d3eb7cad75f8 Extracting 72 s
 d3eb7cad75f8 Extracting 72 s
 d3eb7cad75f8 Extracting 72 s
 d3eb7cad75f8 Extracting 72 s
 d3eb7cad75f8 Extracting 73 s
 d3eb7cad75f8 Extracting 73 s
 d3eb7cad75f8 Extracting 73 s
 d3eb7cad75f8 Extracting 73 s
 d3eb7cad75f8 Extracting 73 s
 d3eb7cad75f8 Extracting 73 s
 d3eb7cad75f8 Extracting 73 s
 d3eb7cad75f8 Extracting 73 s
 d3eb7cad75f8 Extracting 73 s
 d3eb7cad75f8 Extracting 73 s
 d3eb7cad75f8 Extracting 74 s
 d3eb7cad75f8 Extracting 74 s
 d3eb7cad75f8 Extracting 74 s
 d3eb7cad75f8 Extracting 74 s
 d3eb7cad75f8 Extracting 74 s
 d3eb7cad75f8 Extracting 74 s
 d3eb7cad75f8 Extracting 74 s
 d3eb7cad75f8 Extracting 74 s
 d3eb7cad75f8 Extracting 74 s
 d3eb7cad75f8 Extracting 74 s
 d3eb7cad75f8 Extracting 75 s
 d3eb7cad75f8 Extracting 75 s
 d3eb7cad75f8 Extracting 75 s
 d3eb7cad75f8 Extracting 75 s
 d3eb7cad75f8 Extracting 75 s
 d3eb7cad75f8 Extracting 75 s
 d3eb7cad75f8 Extracting 75 s
 d3eb7cad75f8 Extracting 75 s
 d3eb7cad75f8 Extracting 75 s
 d3eb7cad75f8 Extracting 76 s
 d3eb7cad75f8 Extracting 76 s
 d3eb7cad75f8 Extracting 76 s
 d3eb7cad75f8 Extracting 76 s
 d3eb7cad75f8 Extracting 76 s
 d3eb7cad75f8 Extracting 76 s
 d3eb7cad75f8 Extracting 76 s
 d3eb7cad75f8 Extracting 76 s
 d3eb7cad75f8 Extracting 76 s
 d3eb7cad75f8 Extracting 76 s
 d3eb7cad75f8 Extracting 76 s
 d3eb7cad75f8 Extracting 77 s
 d3eb7cad75f8 Extracting 77 s
 d3eb7cad75f8 Extracting 77 s
 d3eb7cad75f8 Extracting 77 s
 d3eb7cad75f8 Extracting 77 s
 d3eb7cad75f8 Extracting 77 s
 d3eb7cad75f8 Extracting 77 s
 d3eb7cad75f8 Extracting 77 s
 d3eb7cad75f8 Extracting 77 s
 d3eb7cad75f8 Extracting 77 s
 d3eb7cad75f8 Extracting 78 s
 d3eb7cad75f8 Extracting 78 s
 d3eb7cad75f8 Extracting 78 s
 d3eb7cad75f8 Extracting 78 s
 d3eb7cad75f8 Extracting 78 s
 d3eb7cad75f8 Extracting 78 s
 d3eb7cad75f8 Extracting 78 s
 d3eb7cad75f8 Extracting 78 s
 d3eb7cad75f8 Extracting 78 s
 d3eb7cad75f8 Extracting 78 s
 d3eb7cad75f8 Extracting 79 s
 d3eb7cad75f8 Extracting 79 s
 d3eb7cad75f8 Extracting 79 s
 d3eb7cad75f8 Extracting 79 s
 d3eb7cad75f8 Extracting 79 s
 d3eb7cad75f8 Extracting 79 s
 d3eb7cad75f8 Extracting 79 s
 d3eb7cad75f8 Extracting 79 s
 d3eb7cad75f8 Extracting 79 s
 d3eb7cad75f8 Extracting 79 s
 d3eb7cad75f8 Extracting 80 s
 d3eb7cad75f8 Extracting 80 s
 d3eb7cad75f8 Extracting 80 s
 d3eb7cad75f8 Extracting 80 s
 d3eb7cad75f8 Extracting 80 s
 d3eb7cad75f8 Extracting 80 s
 d3eb7cad75f8 Extracting 80 s
 d3eb7cad75f8 Extracting 80 s
 d3eb7cad75f8 Extracting 80 s
 d3eb7cad75f8 Extracting 81 s
 d3eb7cad75f8 Extracting 81 s
 d3eb7cad75f8 Extracting 81 s
 d3eb7cad75f8 Extracting 81 s
 d3eb7cad75f8 Extracting 81 s
 d3eb7cad75f8 Extracting 81 s
 d3eb7cad75f8 Extracting 81 s
 d3eb7cad75f8 Extracting 81 s
 d3eb7cad75f8 Extracting 81 s
 d3eb7cad75f8 Extracting 81 s
 d3eb7cad75f8 Extracting 81 s
 d3eb7cad75f8 Extracting 82 s
 d3eb7cad75f8 Extracting 82 s
 d3eb7cad75f8 Extracting 82 s
 d3eb7cad75f8 Extracting 82 s
 d3eb7cad75f8 Extracting 82 s
 d3eb7cad75f8 Extracting 82 s
 d3eb7cad75f8 Extracting 82 s
 d3eb7cad75f8 Extracting 82 s
 d3eb7cad75f8 Extracting 82 s
 d3eb7cad75f8 Extracting 83 s
 d3eb7cad75f8 Extracting 83 s
 d3eb7cad75f8 Extracting 83 s
 d3eb7cad75f8 Extracting 83 s
 d3eb7cad75f8 Extracting 83 s
 d3eb7cad75f8 Extracting 83 s
 d3eb7cad75f8 Extracting 83 s
 d3eb7cad75f8 Extracting 83 s
 d3eb7cad75f8 Extracting 83 s
 d3eb7cad75f8 Extracting 83 s
 d3eb7cad75f8 Extracting 83 s
 d3eb7cad75f8 Extracting 84 s
 d3eb7cad75f8 Extracting 84 s
 d3eb7cad75f8 Extracting 84 s
 d3eb7cad75f8 Extracting 84 s
 d3eb7cad75f8 Extracting 84 s
 d3eb7cad75f8 Extracting 84 s
 d3eb7cad75f8 Extracting 84 s
 d3eb7cad75f8 Extracting 84 s
 d3eb7cad75f8 Extracting 84 s
 d3eb7cad75f8 Extracting 84 s
 d3eb7cad75f8 Extracting 85 s
 d3eb7cad75f8 Extracting 85 s
 d3eb7cad75f8 Extracting 85 s
 d3eb7cad75f8 Extracting 85 s
 d3eb7cad75f8 Extracting 85 s
 d3eb7cad75f8 Extracting 85 s
 d3eb7cad75f8 Extracting 85 s
 d3eb7cad75f8 Extracting 85 s
 d3eb7cad75f8 Extracting 85 s
 d3eb7cad75f8 Extracting 85 s
 d3eb7cad75f8 Extracting 86 s
 d3eb7cad75f8 Extracting 86 s
 d3eb7cad75f8 Extracting 86 s
 d3eb7cad75f8 Extracting 86 s
 d3eb7cad75f8 Extracting 86 s
 d3eb7cad75f8 Extracting 86 s
 d3eb7cad75f8 Extracting 86 s
 d3eb7cad75f8 Extracting 86 s
 d3eb7cad75f8 Extracting 86 s
 d3eb7cad75f8 Extracting 86 s
 d3eb7cad75f8 Extracting 87 s
 d3eb7cad75f8 Extracting 87 s
 d3eb7cad75f8 Extracting 87 s
 d3eb7cad75f8 Extracting 87 s
 d3eb7cad75f8 Extracting 87 s
 d3eb7cad75f8 Extracting 87 s
 d3eb7cad75f8 Extracting 87 s
 d3eb7cad75f8 Extracting 87 s
 d3eb7cad75f8 Extracting 87 s
 d3eb7cad75f8 Extracting 87 s
 d3eb7cad75f8 Extracting 88 s
 d3eb7cad75f8 Extracting 88 s
 d3eb7cad75f8 Extracting 88 s
 d3eb7cad75f8 Extracting 88 s
 d3eb7cad75f8 Extracting 88 s
 d3eb7cad75f8 Extracting 88 s
 d3eb7cad75f8 Extracting 88 s
 d3eb7cad75f8 Extracting 88 s
 d3eb7cad75f8 Extracting 88 s
 d3eb7cad75f8 Extracting 89 s
 d3eb7cad75f8 Extracting 89 s
 d3eb7cad75f8 Extracting 89 s
 d3eb7cad75f8 Extracting 89 s
 d3eb7cad75f8 Extracting 89 s
 d3eb7cad75f8 Extracting 89 s
 d3eb7cad75f8 Extracting 89 s
 d3eb7cad75f8 Extracting 89 s
 d3eb7cad75f8 Extracting 89 s
 d3eb7cad75f8 Extracting 89 s
 d3eb7cad75f8 Extracting 89 s
 d3eb7cad75f8 Extracting 90 s
 d3eb7cad75f8 Extracting 90 s
 d3eb7cad75f8 Extracting 90 s
 d3eb7cad75f8 Extracting 90 s
 d3eb7cad75f8 Extracting 90 s
 d3eb7cad75f8 Extracting 90 s
 d3eb7cad75f8 Extracting 90 s
 d3eb7cad75f8 Extracting 90 s
 d3eb7cad75f8 Extracting 90 s
 d3eb7cad75f8 Extracting 91 s
 d3eb7cad75f8 Extracting 91 s
 d3eb7cad75f8 Extracting 91 s
 d3eb7cad75f8 Extracting 91 s
 d3eb7cad75f8 Extracting 91 s
 d3eb7cad75f8 Extracting 91 s
 d3eb7cad75f8 Extracting 91 s
 d3eb7cad75f8 Extracting 91 s
 d3eb7cad75f8 Extracting 91 s
 d3eb7cad75f8 Extracting 91 s
 d3eb7cad75f8 Extracting 91 s
 d3eb7cad75f8 Extracting 92 s
 d3eb7cad75f8 Extracting 92 s
 d3eb7cad75f8 Extracting 92 s
 d3eb7cad75f8 Extracting 92 s
 d3eb7cad75f8 Extracting 92 s
 d3eb7cad75f8 Extracting 92 s
 d3eb7cad75f8 Extracting 92 s
 d3eb7cad75f8 Extracting 92 s
 d3eb7cad75f8 Extracting 92 s
 d3eb7cad75f8 Extracting 92 s
 d3eb7cad75f8 Extracting 93 s
 d3eb7cad75f8 Extracting 93 s
 d3eb7cad75f8 Extracting 93 s
 d3eb7cad75f8 Extracting 93 s
 d3eb7cad75f8 Extracting 93 s
 d3eb7cad75f8 Extracting 93 s
 d3eb7cad75f8 Extracting 93 s
 d3eb7cad75f8 Extracting 93 s
 d3eb7cad75f8 Extracting 93 s
 d3eb7cad75f8 Extracting 93 s
 d3eb7cad75f8 Extracting 94 s
 d3eb7cad75f8 Extracting 94 s
 d3eb7cad75f8 Extracting 94 s
 d3eb7cad75f8 Extracting 94 s
 d3eb7cad75f8 Extracting 94 s
 d3eb7cad75f8 Extracting 94 s
 d3eb7cad75f8 Extracting 94 s
 d3eb7cad75f8 Extracting 94 s
 d3eb7cad75f8 Extracting 94 s
 d3eb7cad75f8 Extracting 95 s
 d3eb7cad75f8 Extracting 95 s
 d3eb7cad75f8 Extracting 95 s
 d3eb7cad75f8 Extracting 95 s
 d3eb7cad75f8 Extracting 95 s
 d3eb7cad75f8 Extracting 95 s
 d3eb7cad75f8 Pull complete 
 466817520ca7 Extracting 1 s
 466817520ca7 Pull complete 
 b0f1a56d391d Extracting 1 s
 b0f1a56d391d Pull complete 
 omi-tasks-supabase-n8n Pulled 
 Volume omi-tasks-supabase_omi-tasks-supabase-n8n-data  Creating
 Volume omi-tasks-supabase_omi-tasks-supabase-n8n-data  Created
time="2026-05-10T22:08:48Z" level=warning msg="Found orphan containers ([omi-tasks-supabase-web omi-tasks-supabase-test-db]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up."
 Container omi-tasks-supabase-n8n  Creating
 Container omi-tasks-supabase-n8n  Created
 Container omi-tasks-supabase-n8n  Starting
 Container omi-tasks-supabase-n8n  Started
Containers:
omi-tasks-supabase-n8n	Up 1 second	0.0.0.0:5679->5678/tcp, [::]:5679->5678/tcp
omi-tasks-supabase-web	Up 2 minutes	0.0.0.0:8098->8098/tcp, [::]:8098->8098/tcp
omi-tasks-supabase-test-db	Up 2 minutes (healthy)	0.0.0.0:55433->5432/tcp, [::]:55433->5432/tcp

Web UI: http://localhost:8098/review
n8n:    http://localhost:5679

Install complete.
- PASS: web health endpoint returns ok
- PASS: review page reachable
- PASS: new task page reachable
- PASS: primary tasks page reachable
- PASS: submissions page reachable
- PASS: trash page reachable
- PASS: status page reachable
- PASS: n8n endpoint becomes reachable
- PASS: Postgres remains running after web startup
- PASS: tasks schema tables exist
- PASS: source systems seeded

## 5. Task candidate review lifecycle

INSERT 0 1
INSERT 0 1
- PASS: two task candidates inserted
- PASS: review page shows seeded candidate
- PASS: candidate approved into primary task
- PASS: candidate marked approved
- PASS: primary page shows approved task
- PASS: candidate rejection recorded

## 6. Task edit, trash, restore, scratch creation

- PASS: task edit saved
- PASS: trash marks task trashed
- PASS: trash page shows task
- PASS: restore returns task to open
- PASS: scratch task created
- PASS: submissions page shows audit trail
- PASS: audit log captured actions

## 7. Pre-uninstall summary

Candidates: 2
Tasks: 2
Audit rows: 6
Containers before uninstall:
- omi-tasks-supabase-n8n :: Up 13 seconds
- omi-tasks-supabase-web :: Up 2 minutes
- omi-tasks-supabase-test-db :: Up 3 minutes (healthy)

## 8. Full uninstall and verification

`./install.sh uninstall --yes`
 Container omi-tasks-supabase-web  Stopping
 Container omi-tasks-supabase-web  Stopped
 Container omi-tasks-supabase-web  Removing
 Container omi-tasks-supabase-web  Removed
 Container omi-tasks-supabase-test-db  Stopping
 Container omi-tasks-supabase-n8n  Stopping
 Container omi-tasks-supabase-test-db  Stopped
 Container omi-tasks-supabase-test-db  Removing
 Container omi-tasks-supabase-test-db  Removed
 Container omi-tasks-supabase-n8n  Stopped
 Container omi-tasks-supabase-n8n  Removing
 Container omi-tasks-supabase-n8n  Removed
 Image omi-tasks-supabase-omi-tasks-supabase-web:latest  Removing
 Network omi-tasks-supabase_default  Removing
 Network omi-tasks-supabase_default  Removed
 Image omi-tasks-supabase-omi-tasks-supabase-web:latest  Removed
 Volume omi-tasks-supabase_omi-tasks-supabase-n8n-data  Removing
 Volume omi-tasks-supabase_omi-tasks-supabase-n8n-data  Removed
Uninstall complete. Only repository files should remain.
- PASS: no OMI-Tasks containers remain
- PASS: no OMI-Tasks Docker volumes remain
- PASS: no OMI-Tasks Docker networks remain
- PASS: generated .env removed
- PASS: repo files still exist
- PASS: working tree remains clean

## 9. Result

- Passed checks: 33
- Failed checks: 0
- Test completed: 2026-05-10T22:09:12+00:00
\n**Overall result: PASS**
