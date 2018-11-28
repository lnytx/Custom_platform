/*
 Highcharts JS v6.0.4 (2017-12-15)
 Drag-panes module

 (c) 2010-2017 Highsoft AS
 Author: Kacper Madej

 License: www.highcharts.com/license
*/
(function(f){"object"===typeof module&&module.exports?module.exports=f:f(Highcharts)})(function(f){(function(b){var f=b.hasTouch,v=b.merge,t=b.wrap,n=b.each,w=b.isNumber,k=b.addEvent,u=b.relativeLength,x=b.objectEach,p=b.Axis,y=b.Pointer;v(!0,p.prototype.defaultYAxisOptions,{minLength:"10%",maxLength:"100%",resize:{controlledAxis:{next:[],prev:[]},enabled:!1,cursor:"ns-resize",lineColor:"#cccccc",lineDashStyle:"Solid",lineWidth:4,x:0,y:0}});b.AxisResizer=function(a){this.init(a)};b.AxisResizer.prototype=
{init:function(a,d){this.axis=a;this.options=a.options.resize;this.render();d||this.addMouseEvents()},render:function(){var a=this.axis,d=a.chart,c=this.options,b=c.x,e=c.y,l=Math.min(Math.max(a.top+a.height+e,d.plotTop),d.plotTop+d.plotHeight),m;m={cursor:c.cursor,stroke:c.lineColor,"stroke-width":c.lineWidth,dashstyle:c.lineDashStyle};this.lastPos=l-e;this.controlLine||(this.controlLine=d.renderer.path().addClass("highcharts-axis-resizer"));this.controlLine.add(a.axisGroup);m.d=d.renderer.crispLine(["M",
a.left+b,l,"L",a.left+a.width+b,l],c.lineWidth);this.controlLine.attr(m)},addMouseEvents:function(){var a=this,d=a.controlLine.element,c=a.axis.chart.container,b=[],e,l,m;a.mouseMoveHandler=e=function(c){a.onMouseMove(c)};a.mouseUpHandler=l=function(c){a.onMouseUp(c)};a.mouseDownHandler=m=function(c){a.onMouseDown(c)};b.push(k(c,"mousemove",e),k(c.ownerDocument,"mouseup",l),k(d,"mousedown",m));f&&b.push(k(c,"touchmove",e),k(c.ownerDocument,"touchend",l),k(d,"touchstart",m));a.eventsToUnbind=b},onMouseMove:function(a){a.touches&&
0===a.touches[0].pageX||!this.grabbed||(this.hasDragged=!0,this.updateAxes(this.axis.chart.pointer.normalize(a).chartY-this.options.y))},onMouseUp:function(a){this.hasDragged&&this.updateAxes(this.axis.chart.pointer.normalize(a).chartY-this.options.y);this.grabbed=this.hasDragged=this.axis.chart.activeResizer=null},onMouseDown:function(){this.axis.chart.pointer.reset(!1,0);this.grabbed=this.axis.chart.activeResizer=!0},updateAxes:function(a){var d=this,c=d.axis.chart,f=d.options.controlledAxis,e=
0===f.next.length?[b.inArray(d.axis,c.yAxis)+1]:f.next,f=[d.axis].concat(f.prev),l=[],m=!1,k=c.plotTop,p=c.plotHeight,r=k+p,q;a=Math.max(Math.min(a,r),k);q=a-d.lastPos;1>q*q||(n([f,e],function(b,f){n(b,function(b,h){var g=(b=w(b)?c.yAxis[b]:f||h?c.get(b):b)&&b.options,e,n;g&&(h=b.top,n=Math.round(u(g.minLength,p)),e=Math.round(u(g.maxLength,p)),f?(q=a-d.lastPos,g=Math.round(Math.min(Math.max(b.len-q,n),e)),h=b.top+q,h+g>r&&(e=r-g-h,a+=e,h+=e),h<k&&(h=k,h+g>r&&(g=p)),g===n&&(m=!0),l.push({axis:b,options:{top:Math.round(h),
height:g}})):(g=Math.round(Math.min(Math.max(a-h,n),e)),g===e&&(m=!0),a=h+g,l.push({axis:b,options:{height:g}})))})}),m||(n(l,function(a){a.axis.update(a.options,!1)}),c.redraw(!1)))},destroy:function(){var a=this;delete a.axis.resizer;this.eventsToUnbind&&n(this.eventsToUnbind,function(a){a()});a.controlLine.destroy();x(a,function(b,c){a[c]=null})}};p.prototype.keepProps.push("resizer");t(p.prototype,"render",function(a){a.apply(this,Array.prototype.slice.call(arguments,1));var d=this.resizer,c=
this.options.resize;c&&(c=!1!==c.enabled,d?c?d.init(this,!0):d.destroy():c&&(this.resizer=new b.AxisResizer(this)))});t(p.prototype,"destroy",function(a,b){!b&&this.resizer&&this.resizer.destroy();a.apply(this,Array.prototype.slice.call(arguments,1))});t(y.prototype,"runPointActions",function(a){this.chart.activeResizer||a.apply(this,Array.prototype.slice.call(arguments,1))})})(f)});
