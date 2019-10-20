<template>
  <v-app>
    <Header/>
    <v-content id="main-background">
      <v-container fluid class="fill-height">
        <v-row style="height:85%">
          <v-col cols="2" class="fill-height">
            <v-sheet color="transparent" class="fill-height pa-5">
              <h1>Altitude</h1>
              <v-slider :disabled="disabled" readonly :min="0" :max="37000" v-model="altitude" color="white" vertical
                        class="large-slider" thumb-label="always" thumb-color="red"></v-slider>
            </v-sheet>
          </v-col>
          <v-col cols="7" class="fill-height">
            <v-sheet color="transparent" class="fill-height pa-5">
              <div class="viewer elevation-6">
                <cesium-viewer :logo="false" :animation="animation" :baseLayerPicker="baseLayerPicker" :camera="camera"
                               :timeline="timeline" :info-box="infoBox" @ready="ready">
                  <imagery-layer>
                    <bingmaps-imagery-provider url="https://dev.virtualearth.net"
                                               bmKey="AgcbDCAOb9zMfquaT4Z-MdHX4AsHUNvs7xgdHefEA5myMHxZk87NTNgdLbG90IE-"
                                               mapStyle="Aerial"/>
                  </imagery-layer>
                  <cesium-terrain-provider></cesium-terrain-provider>
                </cesium-viewer>
              </div>
            </v-sheet>
          </v-col>
          <v-col cols="3" class="fill-height">
            <v-sheet color="transparent" class="mb-10 pa-5" style="height:40%">
              <h3>Horizon View</h3>
              <v-img @click="openHorizonModal" class="elevation-6" max-width="500px" contain :src="horizonSrc"></v-img>
            </v-sheet>
            <v-sheet color="transparent" class="mt-10 pa-5" style="height:40%">
              <h3>Bottom View</h3>
              <v-img @click="openBottomModal" class="elevation-6" max-width="500px" contain :src="bottomSrc"></v-img>
            </v-sheet>
          </v-col>
        </v-row>
        <v-row style="height:15%">
          <v-col cols="12">
            <v-sheet :min="0" :max="5000" color="black" class="pa-5 elevation-6" style="height:100%">
              <h3>Timeline</h3>
              <v-slider @change="onTimeChange" thumb-label="always" :min="0" :max="allPoints.length ? allPoints.length : 0" :disabled="disabled" v-model="time" color="white"></v-slider>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
    <v-dialog v-model="dialog" max-width="60%">
      <v-card class="pa-4">
        <v-img max-height="100%" contain :src="modalImage"></v-img>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
    import CesiumViewer from 'vue-cesium/src/components/viewer/CesiumViewer.vue'
    import Header from '@/components/Header.vue'
    import axios from 'axios';

    export default {
        name: 'main',
        props: ['id'],
        data: () => ({
            disabled: true,
            time: null,
            altitude: null,
            dialog: false,
            horizonSrc: "https://ethanelliott.ca/2019spaceapps/Stratos_DataSet/TIMMINS2018/CDH/CAM2-HOR/100.jpg",
            bottomSrc: "https://ethanelliott.ca/2019spaceapps/Stratos_DataSet/TIMMINS2018/CDH/CAM1-NADIR/103L.jpg",
            modalImage: null,
            allPoints: [],
            camera: {
                position: {
                    lng: 0,
                    lat: 0,
                    height: 200
                },
                heading: 360,
                pitch: -40,
                roll: 0
            },
            animation: false,
            baseLayerPicker: false,
            timeline: false,
            infoBox: true,
            cesiumInstance: null
        }),
        components: {
            Header,
            CesiumViewer
        },
        methods: {
            onTimeChange() {
                if (this.allPoints[this.time]) {
                    this.altitude = this.allPoints[this.time].altitude;
                }
            },
            openHorizonModal() {
                this.modalImage = this.horizonSrc;
                this.dialog = true;
            },
            openBottomModal() {
                this.modalImage = this.bottomSrc;
                this.dialog = true;
            },
            ready(cesiumInstance) {
                this.cesiumInstance = cesiumInstance;
                const {viewer, Cesium} = this.cesiumInstance;
                viewer.entities.removeAll();
                viewer.entities.add({
                    name: 'Blue dashed line',
                    polyline: {
                        positions: Cesium.Cartesian3.fromDegreesArrayHeights([
                            -80.498378, 43.450941, 294,
                            -80.498378, 43.450941, 500,
                            -80.508378, 43.430941, 1000,
                            -80.528378, 43.420941, 294,
                        ]),
                        width: 4,
                        material: new Cesium.PolylineDashMaterialProperty({
                            color: Cesium.Color.RED
                        })
                    }
                });
                viewer.entities.add(this.drawBalloon(
                    43.450941,
                    -80.498378,
                    0,
                    360,
                    0,
                    0
                ));
                // viewer.trackedEntity = entity;
                this.camera.position.lat = 43.450941;
                this.camera.position.lng = -80.498378;
                this.camera.position.height = 500;
                this.camera.heading = Cesium.Math.toRadians(360);
                this.camera.pitch = -90;
                this.camera.roll = 0;
                this.disabled = false;
            },
            drawBalloon(lat, lon, height, headingDeg, pitch, roll) {
                const {Cesium} = this.cesiumInstance;
                let position = Cesium.Cartesian3.fromDegrees(lon, lat, height + 294.0);
                let heading = Cesium.Math.toRadians(headingDeg);
                let hpr = new Cesium.HeadingPitchRoll(heading, pitch, roll);
                let orientation = Cesium.Transforms.headingPitchRollQuaternion(position, hpr);
                return {
                    name: "Balloon",
                    position: position,
                    orientation: orientation,
                    model: {
                        uri: "/SampleData/models/CesiumBalloon/CesiumBalloon.glb",
                        minimumPixelSize: 64,
                        maximumScale: 1
                    }
                };
            }
        },
        mounted() {
            console.log(this.id);
            axios.get(`http://localhost:5050/visualize?id=${this.id}`)
                .then(res => {
                    this.allPoints = res.data[0].data;
                }).catch(err => {
                console.log(err);
            })
        }
    }
</script>

<style lang="scss">
  .large-slider .v-slider {
    height: 600px;
  }

  .viewer {
    width: 100%;
    height: 650px;
  }
</style>
