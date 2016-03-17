.class public final Lcom/baidu/mobads/SplashAd;
.super Ljava/lang/Object;


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/baidu/mobads/SplashAd$a;
    }
.end annotation


# static fields
.field private static a:Ljava/lang/Class;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/lang/Class",
            "<*>;"
        }
    .end annotation
.end field


# instance fields
.field private b:Ljava/lang/Object;

.field private c:Lcom/baidu/mobads/SplashAdListener;


# direct methods
.method public constructor <init>(Landroid/content/Context;Landroid/view/ViewGroup;Lcom/baidu/mobads/SplashAdListener;)V
    .locals 1

    const-string v0, ""

    invoke-direct {p0, p1, p2, p3, v0}, Lcom/baidu/mobads/SplashAd;-><init>(Landroid/content/Context;Landroid/view/ViewGroup;Lcom/baidu/mobads/SplashAdListener;Ljava/lang/String;)V

    return-void
.end method

.method public constructor <init>(Landroid/content/Context;Landroid/view/ViewGroup;Lcom/baidu/mobads/SplashAdListener;Ljava/lang/String;)V
    .locals 5

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    new-instance v0, Lcom/baidu/mobads/d;

    invoke-direct {v0, p0}, Lcom/baidu/mobads/d;-><init>(Lcom/baidu/mobads/SplashAd;)V

    iput-object v0, p0, Lcom/baidu/mobads/SplashAd;->c:Lcom/baidu/mobads/SplashAdListener;

    :try_start_0
    sget-object v0, Lcom/baidu/mobads/SplashAd;->a:Ljava/lang/Class;

    if-nez v0, :cond_0

    const-string v0, "com.baidu.mobads.remote.SplashAd"

    invoke-static {p1, v0}, Lcom/baidu/mobads/a/b;->b(Landroid/content/Context;Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    sput-object v0, Lcom/baidu/mobads/SplashAd;->a:Ljava/lang/Class;

    :cond_0
    if-eqz p3, :cond_1

    iput-object p3, p0, Lcom/baidu/mobads/SplashAd;->c:Lcom/baidu/mobads/SplashAdListener;

    :cond_1
    new-instance v0, Lcom/baidu/mobads/SplashAd$a;

    iget-object v1, p0, Lcom/baidu/mobads/SplashAd;->c:Lcom/baidu/mobads/SplashAdListener;

    invoke-direct {v0, p0, v1}, Lcom/baidu/mobads/SplashAd$a;-><init>(Lcom/baidu/mobads/SplashAd;Lcom/baidu/mobads/SplashAdListener;)V

    sget-object v1, Lcom/baidu/mobads/SplashAd;->a:Ljava/lang/Class;

    const/4 v2, 0x4

    new-array v2, v2, [Ljava/lang/Class;

    const/4 v3, 0x0

    const-class v4, Landroid/content/Context;

    aput-object v4, v2, v3

    const/4 v3, 0x1

    const-class v4, Landroid/view/ViewGroup;

    aput-object v4, v2, v3

    const/4 v3, 0x2

    const-class v4, Landroid/os/Handler$Callback;

    aput-object v4, v2, v3

    const/4 v3, 0x3

    const-class v4, Ljava/lang/String;

    aput-object v4, v2, v3

    invoke-virtual {v1, v2}, Ljava/lang/Class;->getConstructor([Ljava/lang/Class;)Ljava/lang/reflect/Constructor;

    move-result-object v1

    const/4 v2, 0x4

    new-array v2, v2, [Ljava/lang/Object;

    const/4 v3, 0x0

    aput-object p1, v2, v3

    const/4 v3, 0x1

    aput-object p2, v2, v3

    const/4 v3, 0x2

    aput-object v0, v2, v3

    const/4 v0, 0x3

    aput-object p4, v2, v0

    invoke-virtual {v1, v2}, Ljava/lang/reflect/Constructor;->newInstance([Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    iput-object v0, p0, Lcom/baidu/mobads/SplashAd;->b:Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    :goto_0
    return-void

    :catch_0
    move-exception v0

    invoke-static {v0}, Lcom/baidu/mobads/a/d;->b(Ljava/lang/Throwable;)I

    goto :goto_0
.end method

.method public static setAppSec(Landroid/content/Context;Ljava/lang/String;)V
    .locals 0

    invoke-static {p0, p1}, Lcom/baidu/mobads/AdView;->setAppSec(Landroid/content/Context;Ljava/lang/String;)V

    return-void
.end method

.method public static setAppSid(Landroid/content/Context;Ljava/lang/String;)V
    .locals 0

    invoke-static {p0, p1}, Lcom/baidu/mobads/AdView;->setAppSid(Landroid/content/Context;Ljava/lang/String;)V

    return-void
.end method
