#include <GLUT/GLUT.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <random>
#include <unistd.h>

inline void delay( unsigned long ms )
{
    usleep( ms * 1000 );
}
float blocksize=10;
float spin=0;
float x=0,y=0,z=0;
GLfloat suofangbi=10;
float speed_x=0,speed_y=-90,speed_z=0;
float target_x=0,target_y=0,targer_z=0;//x range from -90 to +90 and y is the same with x
float getram(int a,int b){
return ((float)rand()/RAND_MAX)*(b-a) + a;
}
void getspeed(){
    if((int)target_x==(int)x&&(int)target_y==(int)y){//reach the target
        target_x=getram(-90,90);
        target_y=getram(-90,90);
        return;
    }
    speed_x=target_x-x<0?-0.3f:0.3f;
    speed_y=target_y-y<0?-0.3f:0.3f;
    x+=speed_x;
    y+=speed_y;
    
}
void RenderScene()
{
    // OpenGL命令，清除颜色缓冲区（使用当前设置的颜色）
    glClear(GL_COLOR_BUFFER_BIT);
    glPushMatrix();
    // 把当前绘图颜色设置为红色
    glColor3f(0.0f, 0.0f, 0.0f);
    getspeed();
    glTranslatef(x, y, speed_z);
    
    // OpenGL命令，用当前的绘图颜色绘制一个填充矩形
    glRectf(-blocksize, blocksize, blocksize, -blocksize);
    glPopMatrix();
    
    //suofangbi+=0.1;
    
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(-1000.0/suofangbi, 1000.0/suofangbi, -1000 /suofangbi, 1000 / suofangbi, 1.0, -1.0);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    // 刷新绘图命令，此时所有未执行的OpenGL命令被执行
    glFlush();
    std::cout<<1000.0/suofangbi<<"\n";
    //delay(10);
}
// 设置渲染状态
void SetupRC()
{
    // 设置用于清除窗口的颜色
    glClearColor(1, 1, 1, 1);
}

// 当窗口大小改变时由GLUT函数库调用
void ChangeSize(GLsizei w, GLsizei h)
{
    //
    GLfloat aspectRatio;
    // 防止被0所除
    if (0 == h){
        h = 1;
    }
    // 设置视口为窗口的大小
    glViewport(0, 0, w, h);
    // 选择投影矩阵，并重置坐标系统
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    
    // 计算窗口的纵横比（像素比）
    aspectRatio = (GLfloat) w / (GLfloat) h;    // 定义裁剪区域（根据窗口的纵横比，并使用正投影）
    std::cout<<aspectRatio<<"\n";
    if (w <=h) {// 宽 < 高
        glOrtho(-100.0, 100.0, -100 /aspectRatio, 100 / aspectRatio, 1.0, -1.0);
    } else {// 宽 > 高
        glOrtho(-100.0 * aspectRatio, 100.0 *aspectRatio, -100.0, 100.0, 1.0, -1.0);
    }
    // 选择模型视图矩阵，并重置坐标系统
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}
using namespace std;
void spinDisplay(void)
{
    spin = spin + 2.0;
    if (spin > 360.0)
        spin = spin - 360.0;
    glutPostRedisplay();
}
void mouse(int button, int state, int x, int y)
{
    switch (button) {
        case GLUT_LEFT_BUTTON:
            if (state == GLUT_DOWN)
                glutIdleFunc(spinDisplay);
            break;
        case GLUT_MIDDLE_BUTTON:
            if (state == GLUT_DOWN)
                glutIdleFunc(NULL);
            break;
        default:
            break;
    }
}
int main(int argc, char *argv[])
{
    // 传递命令行参数，并对GLUT函数库进行初始化
    glutInit(&argc, argv);
    // 设置创建窗口时的显示模式（单缓冲区、RGBA颜色模式）
    glutInitDisplayMode(GLUT_SINGLE |GLUT_RGBA);
    glutInitWindowSize (1000, 4000);
    glutInitWindowPosition (100, 100);
    // 创建窗口
    glutCreateWindow("GLRect");
    // 设置显示回调函数
    glutDisplayFunc(RenderScene);
    // 设置当窗口的大小发生变化时的回调函数
    glutReshapeFunc(ChangeSize);
    glutMouseFunc(mouse);
    // 设置渲染状态
    SetupRC();
    //sleep(1000);
    // 启动GLUT框架的运行，一经调用便不再返回，直到程序终止
    glutMainLoop();
    cout<<1;
    return 0;
}