"use client"
import { Navbar, NavbarBrand, NavbarContent, NavbarItem, Link } from "@nextui-org/react";
import logo from "@/public/logo.png"
export default function MyNavBar() {
    const handleLogout = () => {
        localStorage.removeItem('username');
        localStorage.removeItem('avatarUrl');
        localStorage.removeItem('role');
        window.location.href = '/';
    }
    return (
        <Navbar isBordered>
            <NavbarBrand>
                <img src={logo.src} alt="logo" width={100} height={100} />
                <p className="font-bold text-inherit px-4">课程平台</p>
            </NavbarBrand>
            <NavbarContent className="hidden sm:flex gap-4" justify="center">
                <NavbarItem>
                    <Link color="foreground" href="/">
                        首页
                    </Link>
                </NavbarItem>
                <NavbarItem>
                    <Link color="foreground" href="/course">
                        课程
                    </Link>
                </NavbarItem>
                { localStorage.getItem('role') === 'teacher' && (
                <NavbarItem>
                    <Link color="foreground" href="/course/submit">
                        发布课程
                    </Link>
                </NavbarItem>
                )}
            </NavbarContent>
            <NavbarContent justify="end">
                {!localStorage.getItem('username') ? (
                    <NavbarItem className="hidden lg:flex">
                        <Link href="/user">登录</Link>
                    </NavbarItem>
                ) : (
                    <>
                        <NavbarItem className="hidden lg:flex">
                            <Link href={`/user/${localStorage.getItem('username')}`}>个人主页</Link>
                        </NavbarItem>
                        <NavbarItem className="hidden lg:flex">
                            <Link onClick={handleLogout}>退出登录</Link>
                        </NavbarItem>
                    </>
                )}
            </NavbarContent>
        </Navbar>)

}