// @flow
// This is intended to be used in conjunction with svg-sprite-loader.
declare module SvgSprite {
  // Export the type so we can annotate function params with it.
  declare export type SvgSprite = {
    +'id': string;
    +'viewBox': string;
  }
  declare export default SvgSprite
}
