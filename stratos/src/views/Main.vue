<template>
  <v-app>
    <Header/>
    <v-content id="main-background">
      <v-container fluid class="fill-height">
        <v-row style="height:85%">
          <v-col cols="2" class="fill-height">
            <v-sheet color="transparent" class="fill-height pa-5">
              <h1>Altitude (m)</h1>
              <v-slider :disabled="disabled" readonly :min="0" :max="37000" v-model="altitude" color="white" vertical
                        class="large-slider" thumb-label="always"  thumb-size="80"  thumb-color="red"></v-slider>
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
<!--              <h3>Timeline</h3>-->
              <v-btn @click="startAnimation">Timeline</v-btn>
              <v-slider @change="onTimeChange" :min="0"
                        :max="allPoints.length ? allPoints.length : 0" :disabled="disabled" v-model="time"
                        color="white"></v-slider>
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
            time: 0,
            altitude: 0,
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
            cesiumInstance: null,
            balloonPathArray: [],
            debounceMethod: null,
            balloonObject: null,
            animationInterval: null
        }),
        components: {
            Header,
            CesiumViewer
        },
        methods: {
            onTimeChange() {
                if (this.cesiumInstance && this.allPoints[this.time]) {
                    this.debounceMethod()
                }
            },
            startAnimation() {
                let c = this;
                let rate = 200;
                if (c.animationInterval) {
                    clearInterval(c.animationInterval);
                    c.animationInterval = null;
                } else {
                    c.animationInterval = setInterval(() => {
                        c.time += rate;
                        c.debounceMethod();
                    }, 5000)
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
            },
            redrawMap(p) {
                if (this.cesiumInstance && this.allPoints[this.time]) {
                    console.log(p);
                    const {viewer} = this.cesiumInstance;
                    viewer.entities.remove(this.balloonObject);
                    this.redrawPath();
                    this.redrawBalloon(p)
                }
            },
            redrawBalloon(p) {
                const {viewer, Cesium} = this.cesiumInstance;
                this.camera.position.lat = this.allPoints[0].latitude;
                this.camera.position.lng = this.allPoints[0].longitude;
                this.camera.position.height = 1000;
                this.camera.heading = Cesium.Math.toRadians(360);
                this.camera.pitch = -90;
                this.camera.roll = 0;
                this.balloonObject = viewer.entities.add(
                    this.drawBalloon(p.latitude, p.longitude, p.altitude, 0, 0, 0)
                );
            },
            redrawPath() {
                const {viewer, Cesium} = this.cesiumInstance;
                viewer.entities.add({
                    name: 'Red dashed line',
                    polyline: {
                        positions: Cesium.Cartesian3.fromDegreesArrayHeights(this.balloonPathArray),
                        width: 10,
                        // material: new Cesium.PolylineDashMaterialProperty({
                        //     color: Cesium.Color.RED
                        // })
                    }
                });
            },
            drawBalloon(lat, lon, height, headingDeg, pitch, roll) {
                const {Cesium} = this.cesiumInstance;
                let position = Cesium.Cartesian3.fromDegrees(lon, lat, height);
                let heading = Cesium.Math.toRadians(headingDeg);
                let hpr = new Cesium.HeadingPitchRoll(heading, pitch, roll);
                let orientation = Cesium.Transforms.headingPitchRollQuaternion(position, hpr);
                return {
                    name: "Balloon",
                    position: position,
                    orientation: orientation,
                    model: {
                        uri: "/SampleData/models/CesiumBalloon/CesiumBalloon.glb",
                        minimumPixelSize: 128,
                        maximumScale: 200
                    }
                };
            }
        },
        mounted() {
            console.log(this.id);
            let c = this;
            axios.get(`http://localhost:5050/visualize?id=${this.id}`)
                .then(res => {
                    console.log("Got All Points");
                    this.allPoints = res.data[0].data;
                    this.allPoints.forEach(e => {
                        this.balloonPathArray.push(e.longitude);
                        this.balloonPathArray.push(e.latitude);
                        this.balloonPathArray.push(e.altitude);
                    });
                    this.debounceMethod = debounce(() => {
                        console.log(JSON.stringify(c.allPoints[0]));
                        if (c.allPoints[c.time].altitude) {
                            c.altitude = c.allPoints[c.time].altitude;
                            if (c.allPoints[c.time].nadir_image) {
                                let url = c.allPoints[c.time].nadir_image.split('.');
                                url = `${url[0]}L.${url[1]}`;
                                this.bottomSrc = `https://ethanelliott.ca/2019spaceapps/Stratos_DataSet/TIMMINS2018/CDH/${url}`;
                            }
                            if (c.allPoints[c.time].horizon_image) {
                                this.horizonSrc = `https://ethanelliott.ca/2019spaceapps/Stratos_DataSet/TIMMINS2018/CDH/${c.allPoints[c.time].horizon_image}`;
                            }
                            let p = c.allPoints[c.time];
                            c.redrawMap(p);
                        } else {
                            c.redrawMap(c.allPoints[0]);
                        }
                    }, 500, false);
                    this.debounceMethod();
                    this.disabled = false;
                }).catch(err => {
                console.log(err);
            })
        }
    }

    function debounce(func, wait, immediate) {
        let timeout;
        return function() {
            const context = this, args = arguments;
            const later = function () {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    }

</script>

<style lang="scss">
  .large-slider .v-slider {
    height: 600px;
  }

  .viewer {
    width: 100%;
    height: 680px;
  }
</style>
