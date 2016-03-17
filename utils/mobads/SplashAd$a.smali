.class Lcom/baidu/mobads/SplashAd$a;
.super Ljava/lang/Object;

# interfaces
.implements Landroid/os/Handler$Callback;


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/baidu/mobads/SplashAd;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = "a"
.end annotation


# instance fields
.field final synthetic a:Lcom/baidu/mobads/SplashAd;

.field private b:Lcom/baidu/mobads/SplashAdListener;


# direct methods
.method public constructor <init>(Lcom/baidu/mobads/SplashAd;Lcom/baidu/mobads/SplashAdListener;)V
    .locals 0

    iput-object p1, p0, Lcom/baidu/mobads/SplashAd$a;->a:Lcom/baidu/mobads/SplashAd;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    iput-object p2, p0, Lcom/baidu/mobads/SplashAd$a;->b:Lcom/baidu/mobads/SplashAdListener;

    return-void
.end method


# virtual methods
.method public handleMessage(Landroid/os/Message;)Z
    .locals 6

    const/4 v5, 0x0

    :try_start_0
    invoke-virtual {p1}, Landroid/os/Message;->getData()Landroid/os/Bundle;

    move-result-object v0

    const-string v1, "method"

    invoke-virtual {v0, v1}, Landroid/os/Bundle;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    const/4 v2, 0x2

    new-array v2, v2, [Ljava/lang/Object;

    const/4 v3, 0x0

    const-string v4, "SplashAd.setSplashListener handleMessage"

    aput-object v4, v2, v3

    const/4 v3, 0x1

    aput-object v0, v2, v3

    invoke-static {v2}, Lcom/baidu/mobads/a/d;->a([Ljava/lang/Object;)I

    const-string v2, "onAdDismissed"

    invoke-virtual {v2, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_1

    iget-object v0, p0, Lcom/baidu/mobads/SplashAd$a;->b:Lcom/baidu/mobads/SplashAdListener;

    invoke-interface {v0}, Lcom/baidu/mobads/SplashAdListener;->onAdDismissed()V

    :cond_0
    :goto_0
    return v5

    :cond_1
    const-string v2, "onAdFailed"

    invoke-virtual {v2, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_2

    const-string v1, "p_reason"

    invoke-virtual {v0, v1}, Landroid/os/Bundle;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    iget-object v1, p0, Lcom/baidu/mobads/SplashAd$a;->b:Lcom/baidu/mobads/SplashAdListener;

    invoke-interface {v1, v0}, Lcom/baidu/mobads/SplashAdListener;->onAdFailed(Ljava/lang/String;)V

    iget-object v0, p0, Lcom/baidu/mobads/SplashAd$a;->b:Lcom/baidu/mobads/SplashAdListener;

    invoke-interface {v0}, Lcom/baidu/mobads/SplashAdListener;->onAdDismissed()V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    :catch_0
    move-exception v0

    invoke-static {v0}, Lcom/baidu/mobads/a/d;->b(Ljava/lang/Throwable;)I

    goto :goto_0

    :cond_2
    :try_start_1
    const-string v0, "onSplashAdPresent"

    invoke-virtual {v0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_0

    iget-object v0, p0, Lcom/baidu/mobads/SplashAd$a;->b:Lcom/baidu/mobads/SplashAdListener;

    invoke-interface {v0}, Lcom/baidu/mobads/SplashAdListener;->onAdPresent()V
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_0

    goto :goto_0
.end method
