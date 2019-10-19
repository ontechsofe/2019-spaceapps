<template>
  <v-app>
    <Header/>
    <v-content id="main-background">
      <v-container fluid class="fill-height">
        <v-row style="height:85%">
          <v-col cols="2" class="fill-height">
            <v-sheet color="transparent" class="fill-height pa-5">
              <h1>Altitude</h1>
              <v-slider readonly :min="0" :max="5000" v-model="altitude" color="white" vertical class="large-slider" thumb-label="always" thumb-color="red"></v-slider>
            </v-sheet>
          </v-col>
          <v-col cols="7" class="fill-height">
            <v-sheet color="transparent" class="fill-height pa-5">
              <div class="viewer elevation-6">
                <cesium-viewer :animation="animation" :baseLayerPicker="baseLayerPicker" :camera="camera" :timeline="timeline" :info-box="infoBox" @ready="ready">
                  <imagery-layer>
                    <bingmaps-imagery-provider url="https://dev.virtualearth.net" bmKey="AgcbDCAOb9zMfquaT4Z-MdHX4AsHUNvs7xgdHefEA5myMHxZk87NTNgdLbG90IE-" mapStyle="Aerial"/>
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
              <v-slider v-model="slider" color="white"></v-slider>
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

    export default {
        name: 'main',
        props: ['id'],
        data: () => ({
            altitude: null,
            slider: null,
            dialog: false,
            horizonSrc: "https://ethanelliott.ca/2019spaceapps/Stratos_DataSet/TIMMINS2018/CDH/CAM2-HOR/100.jpg",
            bottomSrc: "https://ethanelliott.ca/2019spaceapps/Stratos_DataSet/TIMMINS2018/CDH/CAM1-NADIR/103L.jpg",
            modalImage: null,
            allPoints: [],
            camera: {
                position: {
                    lng:  -80.498378,
                    lat: 43.450941,
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
            openHorizonModal() {
                this.modalImage = this.horizonSrc;
                this.dialog = true;
            },
            openBottomModal() {
                this.modalImage = this.bottomSrc;
                this.dialog = true;
            },
            ready (cesiumInstance) {
                this.cesiumInstance = cesiumInstance;
                const {viewer} = this.cesiumInstance;
                viewer.entities.removeAll();
                let entity = viewer.entities.add(this.drawBalloon(
                    43.450941,
                    -80.498378,
                    0,
                    360,
                    0,
                    0
                ));
                viewer.trackedEntity = entity;
            },
            drawBalloon(lat, lon, height, headingDeg, pitch, roll) {
                const {Cesium} = this.cesiumInstance;
                let position = Cesium.Cartesian3.fromDegrees(lon, lat, height + 294.0);
                let heading = Cesium.Math.toRadians(headingDeg);
                let hpr = new Cesium.HeadingPitchRoll(heading, pitch, roll);
                let orientation = Cesium.Transforms.headingPitchRollQuaternion(position, hpr);
                return {
                    name : "/SampleData/models/CesiumBalloon/CesiumBalloon.glb",
                    position : position,
                    orientation : orientation,
                    model : {
                        uri : "/SampleData/models/CesiumBalloon/CesiumBalloon.glb",
                        minimumPixelSize : 64,
                        maximumScale : 1
                    }
                };
            }
        },
        mounted() {
            console.log(this.id);
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
